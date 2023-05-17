from datetime import datetime
from classy import Classy, mutable, immutable
import pytest


def test_decorator_marks_mutability_attribute() -> None:
    @mutable
    class Mutable(Classy):
        name: str

    @immutable
    class Immutable(Classy):
        name: str

    assert hasattr(Mutable, "_Mutable__mutable_object")
    assert not hasattr(Mutable, "_Mutable__immutable_object")
    assert getattr(Mutable, "_Mutable__mutable_object") == True

    assert hasattr(Immutable, "_Immutable__immutable_object")
    assert not hasattr(Immutable, "_Immutable__mutable_object")
    assert getattr(Immutable, "_Immutable__immutable_object") == True


def test_classy_object_with_not_mutability_decorator_raises_error() -> None:
    class WithoutDecorator(Classy):
        name: str

    class ButDefinesInit(Classy):
        name: str

        def __init__(self) -> None:
            ...

    class LooksLikeRightClass(Classy):
        name: str

        def __init__(self, name: str) -> None:
            self.name = name

    with pytest.raises(TypeError):
        w1: WithoutDecorator = WithoutDecorator()
    with pytest.raises(TypeError):
        w2: ButDefinesInit = ButDefinesInit()
    with pytest.raises(TypeError):
        w3: LooksLikeRightClass = LooksLikeRightClass(name="john")


def test_decorator_cannot_cross_inherit() -> None:
    @mutable
    class Parent(Classy):
        name: str
        age: int

    with pytest.raises(TypeError):

        @immutable  # type: ignore
        class Child(Parent):
            birthday: datetime


def test_classy_object_from_to_dict() -> None:
    @immutable
    class Student(Classy):
        name: str

        def __hash__(self) -> int:
            return hash(self.name)

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Student):
                return False
            return self.name == __o.name

    @immutable
    class Class(Classy):
        name: str
        student: Student
        students_list: list[Student]
        students_dict: dict[str, Student]
        random_things: tuple[str, int, Student]

        def __hash__(self) -> int:
            return (
                hash(self.name)
                ^ hash(self.student)
                ^ hash(self.students_list)
                ^ hash(self.random_things)
            )

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Class):
                return False
            return (
                self.name == __o.name
                and self.student == __o.student
                and self.students_list == __o.students_list
                and self.students_dict == __o.students_dict
                and self.random_things == __o.random_things
            )

    assert Class(
        name="Software Engineering",
        student=Student(name="Sarah"),
        students_list=[
            Student(name="John"),
            Student(name="Sarah"),
            Student(name="Michael"),
        ],
        students_dict={
            "John": Student(name="John"),
            "Sarah": Student(name="Sarah"),
            "Michael": Student(name="Michael"),
        },
        random_things=("random", 0, Student(name="John")),
    ).dict == {
        "name": "Software Engineering",
        "student": {"name": "Sarah"},
        "students_list": [
            {"name": "John"},
            {"name": "Sarah"},
            {"name": "Michael"},
        ],
        "students_dict": {
            "John": {"name": "John"},
            "Sarah": {"name": "Sarah"},
            "Michael": {"name": "Michael"},
        },
        "random_things": ("random", 0, {"name": "John"}),
    }
    assert Class.from_dict(
        {
            "name": "Software Engineering",
            "student": {"name": "Sarah"},
            "students_list": [
                {"name": "John"},
                {"name": "Sarah"},
                {"name": "Michael"},
            ],
            "students_dict": {
                "John": {"name": "John"},
                "Sarah": {"name": "Sarah"},
                "Michael": {"name": "Michael"},
            },
            "random_things": ("random", 0, {"name": "John"}),
        }
    ) == Class(
        name="Software Engineering",
        student=Student(name="Sarah"),
        students_list=[
            Student(name="John"),
            Student(name="Sarah"),
            Student(name="Michael"),
        ],
        students_dict={
            "John": Student(name="John"),
            "Sarah": Student(name="Sarah"),
            "Michael": Student(name="Michael"),
        },
        random_things=("random", 0, Student(name="John")),
    )


def test_classy_object_from_to_json() -> None:
    @immutable
    class Student(Classy):
        name: str

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Student):
                return False
            return self.name == __o.name

    @immutable
    class Class(Classy):
        name: str
        student: Student
        students_list: list[Student]
        students_dict: dict[str, Student]
        random_things: tuple[str, int, Student]

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Class):
                return False
            return (
                self.name == __o.name
                and self.student == __o.student
                and self.students_list == __o.students_list
                and self.students_dict == __o.students_dict
                and self.random_things == __o.random_things
            )

    assert (
        Class(
            name="Software Engineering",
            student=Student(name="Sarah"),
            students_list=[
                Student(name="John"),
                Student(name="Sarah"),
                Student(name="Michael"),
            ],
            students_dict={
                "John": Student(name="John"),
                "Sarah": Student(name="Sarah"),
                "Michael": Student(name="Michael"),
            },
            random_things=("random", 0, Student(name="John")),
        ).json
        == '{"name":"Software Engineering","student":{"name":"Sarah"},"students_list":[{"name":"John"},{"name":"Sarah"},{"name":"Michael"}],"students_dict":{"John":{"name":"John"},"Sarah":{"name":"Sarah"},"Michael":{"name":"Michael"}},"random_things":["random",0,{"name":"John"}]}'
    )
    assert Class.from_json(
        '{"name":"Software Engineering","student":{"name":"Sarah"},"students_list":[{"name":"John"},{"name":"Sarah"},{"name":"Michael"}],"students_dict":{"John":{"name":"John"},"Sarah":{"name":"Sarah"},"Michael":{"name":"Michael"}},"random_things":["random",0,{"name":"John"}]}'
    ) == Class(
        name="Software Engineering",
        student=Student(name="Sarah"),
        students_list=[
            Student(name="John"),
            Student(name="Sarah"),
            Student(name="Michael"),
        ],
        students_dict={
            "John": Student(name="John"),
            "Sarah": Student(name="Sarah"),
            "Michael": Student(name="Michael"),
        },
        random_things=("random", 0, Student(name="John")),
    )


def test_classy_object_generate_default() -> None:
    @immutable
    class Student(Classy):
        name: str

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Student):
                return False
            return self.name == __o.name

    @immutable
    class Class(Classy):
        name: str
        student: Student
        students_list: list[Student]
        students_dict: dict[str, Student]
        random_things: tuple[str, int, Student]

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Class):
                return False
            return (
                self.name == __o.name
                and self.student == __o.student
                and self.students_list == __o.students_list
                and self.students_dict == __o.students_dict
                and self.random_things == __o.random_things
            )

    assert Class.default() == Class(
        name="",
        student=Student.default(),
        students_list=[],
        students_dict={},
        random_things=("", 0, Student.default()),
    )


def test_wrong_type_hint() -> None:
    @immutable
    class Student(Classy):
        name: str

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Student):
                return False
            return self.name == __o.name

    @immutable
    class Class(Classy):
        name: str
        student: Student
        students_list: list[str, Student]  # type: ignore
        students_dict: dict[str, Student]
        random_things: tuple[str, int, Student]

        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, Class):
                return False
            return (
                self.name == __o.name
                and self.student == __o.student
                and self.students_list == __o.students_list
                and self.students_dict == __o.students_dict
                and self.random_things == __o.random_things
            )

    with pytest.raises(TypeError):
        assert Class.from_dict(
            {
                "name": "Software Engineering",
                "student": {"name": "Sarah"},
                "students_list": [
                    {"name": "John"},
                    {"name": "Sarah"},
                    {"name": "Michael"},
                ],
                "students_dict": {
                    "John": {"name": "John"},
                    "Sarah": {"name": "Sarah"},
                    "Michael": {"name": "Michael"},
                },
                "random_things": ("random", 0, {"name": "John"}),
            }
        ) == Class(
            name="Software Engineering",
            student=Student(name="Sarah"),
            students_list=[
                Student(name="John"),
                Student(name="Sarah"),
                Student(name="Michael"),
            ],  # type: ignore
            students_dict={
                "John": Student(name="John"),
                "Sarah": Student(name="Sarah"),
                "Michael": Student(name="Michael"),
            },
            random_things=("random", 0, Student(name="John")),
        )
