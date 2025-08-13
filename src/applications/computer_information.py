import socket
from platform import processor, machine, system, version

from src.domain.config import Config
from src.applications.common.logger_handler import Logger


def get_computer_information(config: Config, logger: Logger) -> None:
    _file_path: str = config["FILE_PATH"]
    _extend: str = config["EXTEND"]
    _information: str = config["SYSTEM_INFORMATION"]
    _path: str = _file_path + _extend + _information

    try:
        with open(_path, "a") as _f:
            if _f.tell() > 10:
                return

            _hostname: str = socket.gethostname()
            _ip: str = socket.gethostbyname("localhost")

            _01: str = f"System: {system()} -> {version()}\n"
            _02: str = f"Processor: {processor()}\n"
            _03: str = f"Machine: {machine()}\n"
            _04: str = f"Hostname: {_hostname} -> {_ip}\n"

            _log: str = _01 + _02 + _03 + _04
            logger.debug(f"writing in {_path}", _log)

            _f.write(_log)
    except Exception as e:
        logger.error("Error in computer information module: \n", e)


# f.write("Private IP Address: " + IPAddr + "\n")
# public_ip = get("https://api.ipify.org").text
# f.write("Public IP Address: " + public_ip + "\n")
