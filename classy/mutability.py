from typing import Type, TypeVar, dataclass_transform
from dataclasses import dataclass

_T = TypeVar("_T")


@dataclass_transform(
    eq_default=False,
    kw_only_default=True,
    frozen_default=False,
)
def mutable(cls: Type[_T]) -> Type[_T]:
    setattr(cls, f"_{cls.__name__}__mutable_object", True)
    return dataclass(eq=False, kw_only=True, frozen=False)(cls)


@dataclass_transform(
    eq_default=False,
    kw_only_default=True,
    frozen_default=True,
)
def immutable(cls: Type[_T]) -> Type[_T]:
    setattr(cls, f"_{cls.__name__}__immutable_object", True)
    return dataclass(eq=False, kw_only=True, frozen=True)(cls)
