from src.domain.config import Config
from src.domain.system_daemon import System_Daemon
from src.applications.common.logger_handler import Logger

# Daemons
from src.applications.daemons.screenshots_interval import Screenshots_Interval
from src.applications.daemons.clipboar_observer import Clipboard_Observer
from src.applications.daemons.keyboard_observer import Keyboard_Observer


def make_daemons(config: Config) -> list[System_Daemon]:
    return [
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
