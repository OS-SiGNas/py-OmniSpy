from typing import NoReturn
from types import FrameType
import signal
import sys
from concurrent.futures import Future, ThreadPoolExecutor

from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger


class Main:
    def __init__(self, logger: Logger, daemons: list[System_Daemon]):
        signal.signal(signal.SIGINT, self.__handle_signals)
        signal.signal(signal.SIGTERM, self.__handle_signals)
        self.__logger: Logger = logger
        self.__futures: list[Future[None]] = []
        self.__daemons: list[System_Daemon] = daemons
        self.__executor = ThreadPoolExecutor(max_workers=len(self.__daemons))

    def init(self) -> None:
        try:
            self.__logger.info("starting")
            for _daemon in self.__daemons:
                self.__futures.append(self.__executor.submit(_daemon.start))
        except Exception as e:
            self.__logger.error("** MainException **", e)
            self.__shutdown(1)

    def __handle_signals(self, signum: int, frame: FrameType | None) -> NoReturn:
        self.__logger.info(f"Signal: {signum} {frame}")
        self.__shutdown(0)
        raise

    def __shutdown(self, code: int) -> None:
        try:
            for _daemon in self.__daemons:
                _daemon.stop()
            for _future in self.__futures:
                self.__logger.warn(f"closing {_future}")
                _future.cancel()
                _future.result(timeout=5)
                self.__logger.info(f"Future: {_future}")
        except Exception as e:
            self.__logger.error("problem in shutdown", e)
        finally:
            self.__executor.shutdown(wait=True, cancel_futures=True)
            self.__futures.clear()
        self.__logger.info("shutdown gracefully!")
        sys.exit(code)
