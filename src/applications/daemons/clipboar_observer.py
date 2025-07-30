import time
import pyperclip

from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger


class Clipboard_Observer(System_Daemon):
    def __init__(self, config: Config, logger: Logger, poll_interval: int = 1):
        self._stop_signal: bool = False
        self._logger: Logger = logger
        self._poll_interval: int = poll_interval
        _file_path: str = config["FILE_PATH"]
        _extend: str = config["EXTEND"]
        _information: str = config["CLIPBOARD_INFORMATION"]
        self._path: str = _file_path + _extend + _information
        logger.info("ready")

    def restart(self): ...
    def stop(self):
        self._logger.info("stopping")
        self._stop_signal = True
        self._poll_interval = 0

    def start(self) -> None:
        self._logger.info("starting")
        _last_clipboard: str = ""
        try:
            while not self._stop_signal:
                _current_clipboard: str = pyperclip.paste()
                if _current_clipboard != _last_clipboard:
                    with open(self._path, "a") as f:
                        f.write(_current_clipboard + "\n---\n")
                    _last_clipboard = _current_clipboard
                    self._logger.info("New content saved")
                time.sleep(5)
        except Exception as e:
            self._logger.error("Error clipboard_listener:", e)
            time.sleep(self._poll_interval)
        finally:
            self._logger.info("Daemon finished")
