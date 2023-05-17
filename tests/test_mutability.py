from dataclasses import FrozenInstanceError
from classy import Classy, mutable, immutable
import pytest


def test_mutable_object_can_mutate_its_field() -> None:
    @mutable
    class Mutable(Classy):
        name: str

    test: Mutable = Mutable(name="John")
    assert test.name == "John"
    test.name = "Sarah"
    assert test.name == "Sarah"


def test_immutable_object_cannot_mutate_its_field() -> None:
    @immutable
    class Mutable(Classy):
        name: str

    test: Mutable = Mutable(name="John")
    assert test.name == "John"
    with pytest.raises(FrozenInstanceError):
        test.name = "Sarah"  # type: ignore
        assert test.name == "Sarah"
