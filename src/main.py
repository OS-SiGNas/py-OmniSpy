from typing import List
from types import FrameType
import signal
import sys
from concurrent.futures import Future, ThreadPoolExecutor

from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger
from src.applications.computer_information import get_computer_information


class Main:
    def __del__(self) -> None:
        self.__logger.info(f"destroying: {self}")
        del self
        breakpoint()

    def __init__(self, config: Config, logger: Logger, daemons: List[System_Daemon]):
        signal.signal(signal.SIGINT, self.__handle_signals)
        signal.signal(signal.SIGTERM, self.__handle_signals)
        self.__logger: Logger = logger
        self.__executor = ThreadPoolExecutor(max_workers=len(daemons))
        self.__daemons = daemons
        self.__futures: list[Future[None]] = []
        try:
            self.__logger.info("starting")
            get_computer_information(config, logger=Logger("Info"))
            for _daemon in daemons:
                self.__futures.append(self.__executor.submit(_daemon.start))
        except Exception as _e:
            self.__logger.error("** MainException **", _e)
            self.__shutdown(1)

    def __handle_signals(self, signum: int, frame: FrameType | None) -> None:
        self.__logger.warn(f"Signal: {signum} {frame}")
        return self.__shutdown(0)

    def __shutdown(self, code: int) -> None:
        try:
            for _daemon in self.__daemons:
                _daemon.stop()
                del _daemon
            for _future in self.__futures:
                self.__logger.warn(f"closing {_future}")
                _future.cancel()
                _future.result(timeout=5)
                self.__logger.info(f"Future: {_future}")
        except Exception as _e:
            self.__logger.error("problem in shutdown", _e)
        finally:
            self.__executor.shutdown(wait=True, cancel_futures=True)
            self.__daemons.clear()
            del self.__daemons
            self.__futures.clear()
            del self.__futures
            del self.__executor
            self.__logger.info("shutdown gracefully!")
            del self.__logger
            del self
            sys.exit(code)
