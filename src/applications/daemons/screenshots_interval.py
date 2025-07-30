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
        self._stop_signal: bool = False
        self._logger: Logger = logger
        self._folder: str = config["FILE_PATH"]
        # _interval = int(config.get("SCREENSHOT_INTERVAL", 60))  # segundos
        self._interval: int = config["SCREENSHOT_INTERVAL"] * 60
        self._number_of_iterations: int = number_of_iterations
        self._number_of_iterations_end: int = number_of_iterations_end
        logger.info("ready")

    def restart(self) -> None: ...
    def stop(self) -> None: 
        self._logger.info("stopping")
        self._stop_signal = True
        self._interval = 0 
        self._number_of_iterations = 0
        self._number_of_iterations_end = 0

    def start(self) -> None:
        self._logger.info("starting")
        while not self._stop_signal and self._number_of_iterations < self._number_of_iterations_end:
            _timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            _filename = f"screenshot_{_timestamp}.png"
            _filepath = f"{self._folder}/{_filename}"
            try:
                _img = ImageGrab.grab()
                self._logger.info("↘️ saving")
                _img.save(_filepath)
                self._logger.info(f"💾 Screenshot saved: {_filepath}")
                self._number_of_iterations += 1
                time.sleep(self._interval)
            except Exception as e:
                self._logger.error(
                    f"Something wrong when take screenshot -> {_filepath}", e
                )
            finally:
                self._logger.info("Daemon finished")