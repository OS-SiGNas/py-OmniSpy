import sounddevice as sd
from scipy.io.wavfile import write

from applications.common.logger_handler import Logger
from domain.config import Config


def microphone_listener(
    config: Config, logger: Logger, microphone_time: int = 10
) -> None:
    logger.info("starting")
    _file_path: str = config["FILE_PATH"]
    _extend: str = config["EXTEND"]
    _information: str = config["AUDIO_INFORMATION"]

    _path: str = _file_path + _extend + _information
    _fs: int = 44100
    _seconds: int = microphone_time

    try:
        _myrecording = sd.rec(int(_seconds * _fs), samplerate=_fs, channels=2)
        sd.wait()
        logger.info(f"Saving: {_path}")
        write(_path, _fs, _myrecording)
    except Exception as e:
        logger.error("Error in microphone_listener", e)
