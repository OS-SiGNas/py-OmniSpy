import datetime


class Logger:
    def __init__(self, name: str):
        self.name = f"[{name}]"

    def _get_date(self) -> str:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_format(self, level: str, date: str, msg: str) -> str:
        return f" {date} {level} {self.name}: {msg}"

    def info(self, msg: str) -> None:
        return print(
            self._get_format(
                level="[INFO]  ",
                date=self._get_date(),
                msg=msg,
            )
        )

    def warn(self, msg: str) -> None:
        return print(
            self._get_format(
                level="[WARN]  ",
                date=self._get_date(),
                msg=msg,
            )
        )

    def debug(self, msg: str, obj: object | None) -> None:
        return print(
            self._get_format(
                level="[DEBUG] ",
                date=self._get_date(),
                msg=msg,
            ),
            obj,
        )

    def error(self, msg: str, error: Exception | None) -> None:
        return print(
            self._get_format(
                level="[ERROR] ",
                date=self._get_date(),
                msg=msg,
            ),
            error,
        )
