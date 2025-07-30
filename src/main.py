from typing import List, NoReturn
from types import FrameType
import signal
import sys
from concurrent.futures import Future, ThreadPoolExecutor

from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger
from src.applications.computer_information import get_computer_information

# Daemons
from src.applications.daemons.screenshots_interval import Screenshots_Interval
from src.applications.daemons.clipboar_observer import Clipboard_Observer
from src.applications.daemons.keyboard_observer import Keyboard_Observer


class Main:
    def __init__(self, config: Config, logger: Logger):
        signal.signal(signal.SIGINT, self._handle_signals)
        signal.signal(signal.SIGTERM, self._handle_signals)
        self._config: Config = config
        self._logger: Logger = logger
        self._futures: list[Future[None]] = []
        self._daemons: List[System_Daemon] = self._get_daemons(config)
        self._executor = ThreadPoolExecutor(max_workers=len(self._daemons))
        try:
            self._logger.info("starting")
            get_computer_information(config, logger=Logger("Info"))
            for daemon in self._daemons:
                self._futures.append(self._executor.submit(daemon.start))
        except Exception as e:
            self._logger.error("** MainException **", e)
            self._shutdown(1)

    def _handle_signals(self, signum: int, frame: FrameType | None) -> NoReturn:
        self._logger.info(f"Signal: {signum} {frame}")
        self._shutdown(0)
        raise

    def _get_daemons(self, config: Config) -> List[System_Daemon]:
        return [
            Screenshots_Interval(
                config,
                logger=Logger("Screenshot_Interval"),
                number_of_iterations=0,
                number_of_iterations_end=3,
            ),
            Clipboard_Observer(
                config,
                logger=Logger("Clipboard_Observer"),
                poll_interval=1,
            ),
            Keyboard_Observer(
                config,
                logger=Logger("Keys_Observer"),
                idle_time_limit=5.0,
            ),
        ]

    def _shutdown(self, code: int) -> None:
        try:
            for daemon in self._daemons:
                daemon.stop()
            for future in self._futures:
                self._logger.warn(f"closing {future}")
                future.cancel()
            for future in self._futures:
                future.result(timeout=5)
                self._logger.info(f"Future: {future}")
        except Exception as e:
            self._logger.error("problem in shutdown", e)
        finally:
            self._executor.shutdown(wait=True, cancel_futures=True)
            self._futures.clear()
        self._logger.info("shutdown gracefully!")
        sys.exit(code)
