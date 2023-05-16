import orjson
from typing import Any, Callable


def orjson_loads(__obj: bytes | bytearray | memoryview | str) -> Any:
    return orjson.loads(__obj)


def orjson_dumps(v, *, default: Callable[[Any], Any] | None = None) -> str:
    return orjson.dumps(v, default=default).decode("UTF-8")
