import time
import datetime
from PIL import ImageGrab

from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger


class Screenshots_Interval(System_Daemon):
    def __init__(
        self,
        config: Config,
        logger: Logger,
        number_of_iterations: int = 0,
        number_of_iterations_end: int = 3,
    ):
        self.__is_running: bool = False
        self.__stop_signal: bool = False
        self.__logger: Logger = logger
        self.__folder: str = config["FILE_PATH"]
        self.__interval: int = config["SCREENSHOT_INTERVAL"] * 60
        self.__number_of_iterations: int = number_of_iterations
        self.__number_of_iterations_end: int = number_of_iterations_end
        self.__logger.info("ready")

    def start(self) -> None:
        if self.__is_running:
            self.__logger.info("daemon is running")
            return None
        self.__logger.info("starting")
        while (
            not self.__stop_signal
            and self.__number_of_iterations < self.__number_of_iterations_end
        ):
            self.__is_running = True
            _timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            _filename = f"screenshot_{_timestamp}.png"
            _filepath = f"{self.__folder}/{_filename}"
            try:
                _img = ImageGrab.grab()
                self.__logger.info("↘️ saving")
                _img.save(_filepath)
                self.__logger.info(f"💾 Screenshot saved: {_filepath}")
                self.__number_of_iterations += 1
                time.sleep(self.__interval)
            except Exception as e:
                self.__logger.error(
                    f"Something wrong when take screenshot -> {_filepath}", e
                )
        self.__is_running = False
        self.__logger.info("Daemon finished")

    def stop(self) -> None:
        if not self.__is_running:
            return None
        self.__logger.info("stopping")
        self.__stop_signal = True

    def restart(self) -> None:
        if not self.__is_running:
            return None
        self.__logger.info("restarting")
        self.stop()
        time.sleep(self.__interval)
        self.start()
