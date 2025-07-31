import time
import pyperclip

from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger


class Clipboard_Observer(System_Daemon):
    def __init__(self, config: Config, logger: Logger, poll_interval: int = 1):
        self.__is_running: bool = False
        self.__stop_signal: bool = False
        self.__logger: Logger = logger
        self.__poll_interval: int = poll_interval
        _file_path: str = config["FILE_PATH"]
        _extend: str = config["EXTEND"]
        _information: str = config["CLIPBOARD_INFORMATION"]
        self.__path: str = _file_path + _extend + _information
        self.__logger.info("ready")

    def restart(self):
        if not self.__is_running:
            self.__logger.info("daemon is not running")
            return None
        self.stop()
        self.start()

    def stop(self):
        if not self.__is_running:
            self.__logger.info("daemon is not running")
            return None
        self.__logger.info("stopping")
        self.__stop_signal = True
        self.__is_running = False

    def start(self) -> None:
        if self.__is_running:
            return None
        self.__logger.info("starting")
        _last_clipboard: str = ""
        try:
            while not self.__stop_signal:
                self.__is_running = True
                _current_clipboard: str = pyperclip.paste()
                if _current_clipboard != _last_clipboard:
                    with open(self.__path, "a") as _f:
                        _f.write(_current_clipboard + "\n---\n")
                    _last_clipboard = _current_clipboard
                    self.__logger.info("New content saved")
                time.sleep(5)
        except Exception as e:
            self.__logger.error("Error clipboard_listener:", e)
            time.sleep(self.__poll_interval)
        finally:
            self.__logger.info("Daemon finished")
