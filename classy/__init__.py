from abc import ABC
from dataclasses import asdict
from datetime import date, datetime, time
from uuid import UUID, uuid4
from types import GenericAlias
from inspect import FullArgSpec, getfullargspec
from typing import Any, Dict, Self, Type, final, get_args
from .serializer import orjson_dumps, orjson_loads
from .mutability import mutable, immutable


class Classy(ABC):
    def __post_init__(self) -> None:
        class_name: str = type(self).__name__
        if not (
            hasattr(self, f"_{class_name}__mutable_object")
            or hasattr(self, f"_{class_name}__immutable_object")
        ):
            raise TypeError(
                f"'{class_name}' not decorated with mutabillity decorator. Domain Object has to decorated with @mutable or @immutable."
            )

    @property
    def dict(self: Any) -> dict[str, Any]:
        return dict(
            [
                (k, v.dict) if isinstance(v, Classy) else (k, v)
                for k, v in asdict(self).items()
                if not k.startswith("_")
            ]
        )

    @property
    def json(self) -> str:
        def default(obj: Any) -> Any:
            if isinstance(obj, set):
                return list(obj)

        return orjson_dumps(self.dict, default=default)

    @classmethod
    def from_json(cls: Type[Self], json: str) -> Self:
        dictionary: dict[str, Any] = orjson_loads(json)
        return cls.from_dict(dictionary)

    @classmethod
    def from_dict(cls: Type[Self], dictionary: Dict[str, Any]) -> Self:
        def get_init_args(cls: Type[Self]) -> dict[str, Type[Any]]:
            argspec: FullArgSpec = getfullargspec(cls.__init__)
            args: dict[str, Type[Any]] = argspec.annotations
            args.pop("return")
            return args

        def decode(__type: Type, __value: Any) -> Any:
            if isinstance(__type, GenericAlias):
                collection_type: type = __type.__origin__
                item_types: tuple[Any, ...] = get_args(__type)
                if collection_type == list:
                    if len(item_types) != 1:
                        raise TypeError("Invalid generic type args.")
                    return [decode(item_types[0], x) for x in __value]
                if collection_type == tuple:
                    if len(item_types) != len(__value):
                        raise TypeError("Invalid generic type args.")
                    return tuple(
                        [
                            decode(item_types[i], x)
                            for i, x in enumerate(__value)
                        ]
                    )
                if collection_type == set:
                    if len(item_types) != 1:
                        raise TypeError("Invalid generic type args.")
                    return {decode(item_types[0], x) for x in __value}
                if collection_type == dict:
                    if len(item_types) != 2:
                        raise TypeError("Invalid generic type args.")
                    return {
                        x: decode(item_types[1], y)
                        for x, y in __value.items()
                        if isinstance(x, item_types[0])
                    }
                raise TypeError(
                    "Unsupported generic type detected in dataclass fields."
                )
            if isinstance(__value, __type):
                return __value
            if issubclass(__type, Classy):
                return __type.from_dict(__value)
            if __type == UUID:
                return UUID(__value)
            if __type == datetime:
                return datetime.fromisoformat(__value)
            if __type == date:
                return date.fromisoformat(__value)
            if __type == time:
                return time.fromisoformat(__value)
            return __value

        init_args: dict[str, type] = get_init_args(cls)
        arg_names: list[str] = list(init_args.keys())
        decoded: dict[str, Any] = dict(
            [
                (k, decode(init_args[k], v))
                for k, v in dictionary.items()
                if k in arg_names
            ]
        )
        return cls(**decoded)

    @classmethod
    def default(cls: Type[Self]) -> Self:
        def __get_constructor_args(cls: Type[Self]) -> dict[str, Type[Any]]:
            argspec: FullArgSpec = getfullargspec(cls.__init__)
            args: dict[str, Type[Any]] = argspec.annotations
            args.pop("return", None)
            return args

        def __default_nested(__type: Type) -> Any:
            if isinstance(__type, GenericAlias):
                collection_type: type = __type.__origin__
                if collection_type == list:
                    return collection_type()
                if collection_type == tuple:
                    item_types: tuple[Any, ...] = get_args(__type)
                    if len(item_types) == 0:
                        return tuple()
                    return tuple([__default_nested(t) for t in item_types])
                if collection_type == set:
                    return collection_type()
                if collection_type == dict:
                    return collection_type()
                raise TypeError(
                    "Unsupported generic type detected in dataclass fields."
                )
            if issubclass(__type, Classy):
                return __type.default()
            if __type == UUID:
                return uuid4()
            if __type == datetime:
                return datetime.now()
            if __type == date:
                return date.today()
            if __type == time:
                return datetime.now().time()
            return __type()

        init_args: dict[str, type] = __get_constructor_args(cls)
        default_dict: dict[str, Any] = dict(
            [(k, __default_nested(t)) for k, t in init_args.items()]
        )
        return cls(**default_dict)
