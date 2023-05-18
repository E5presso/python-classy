from datetime import date, datetime, time
from uuid import UUID, uuid4
from python_classy import Classy, mutable, immutable
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
            return super().equals(__o)

    class ButDefinesInit(Classy):
        name: str

        def __init__(self) -> None:
            ...

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
            return super().equals(__o)

    class LooksLikeRightClass(Classy):
        name: str

        def __init__(self, name: str) -> None:
            self.name = name

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
            return super().equals(__o)

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

        def compute_hash(self) -> int:
            return hash(self.name)

        def equals(self, __o: object) -> bool:
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

        def compute_hash(self) -> int:
            return (
                hash(self.name)
                ^ hash(self.student)
                ^ hash(self.students_list)
                ^ hash(self.random_things)
            )

        def equals(self, __o: object) -> bool:
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
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
        == '{"name": "Software Engineering", "student": {"name": "Sarah"}, "students_list": [{"name": "John"}, {"name": "Sarah"}, {"name": "Michael"}], "students_dict": {"John": {"name": "John"}, "Sarah": {"name": "Sarah"}, "Michael": {"name": "Michael"}}, "random_things": ["random", 0, {"name": "John"}]}'
    )
    assert Class.from_json(
        '{"name": "Software Engineering", "student": {"name": "Sarah"}, "students_list": [{"name": "John"}, {"name": "Sarah"}, {"name": "Michael"}], "students_dict": {"John": {"name": "John"}, "Sarah": {"name": "Sarah"}, "Michael": {"name": "Michael"}}, "random_things": ["random", 0, {"name": "John"}]}'
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
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

        def compute_hash(self) -> int:
            return super().compute_hash()

        def equals(self, __o: object) -> bool:
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


def test_non_equatable() -> None:
    @mutable
    class MutableClass(Classy):
        name: str
        age: int
        job: str

    a: MutableClass = MutableClass(
        name="John",
        age=29,
        job="Doctor",
    )
    b: MutableClass = MutableClass(
        name="John",
        age=29,
        job="Doctor",
    )
    with pytest.raises(NotImplementedError):
        assert a == b


def test_decode_tuple_with_wrong_arg_length() -> None:
    @immutable
    class HaveTuple(Classy):
        tuples: tuple[int, str, str]

    with pytest.raises(TypeError):
        HaveTuple.from_dict({"tuples": (0, "", "", "")})


def test_decode_dict_with_wrong_args() -> None:
    @immutable
    class WithDict(Classy):
        dicts: dict[str, int, int]  # type: ignore

    with pytest.raises(TypeError):
        WithDict.from_dict({"dicts": {"key": 0}})


def test_decode_with_unsupported_generic() -> None:
    @immutable
    class HasSet(Classy):
        sets: set[str]

    with pytest.raises(TypeError):
        HasSet.from_dict({"sets": set(["a", "b", "c"])})


def test_decode_with_various_supported_types() -> None:
    @immutable
    class HasSupportedTypes(Classy):
        id: UUID
        timestamp: datetime
        only_date: date
        only_time: time
        string: str

    id: UUID = uuid4()
    timestamp: datetime = datetime.now()
    only_date: date = date.today()
    only_time: time = datetime.now().time()
    string: str = "a"
    assert HasSupportedTypes.from_dict(
        {
            "id": id.hex,
            "timestamp": timestamp.isoformat(),
            "only_date": only_date.isoformat(),
            "only_time": only_time.isoformat(),
            "string": string,
        }
    ).dict == {
        "id": id,
        "timestamp": timestamp,
        "only_date": only_date,
        "only_time": only_time,
        "string": string,
    }


def test_default_with_tuples() -> None:
    @immutable
    class HasTuple(Classy):
        tuples: tuple[str, str, int, UUID, datetime, date, time]

    default: HasTuple = HasTuple.default()
    assert len(default.tuples) == 7
    assert default.tuples[0] == ""
    assert default.tuples[1] == ""
    assert default.tuples[2] == 0
    assert isinstance(default.tuples[3], UUID)
    assert isinstance(default.tuples[4], datetime)
    assert isinstance(default.tuples[5], date)
    assert isinstance(default.tuples[6], time)


def test_classy_eq_ne_hash() -> None:
    @immutable
    class Test(Classy):
        name: str

        def equals(self, __o: object) -> bool:
            if not isinstance(__o, Test):
                return False
            return self.name == __o.name

        def compute_hash(self) -> int:
            return hash(self.name)

    t1: Test = Test(name="John")
    t2: Test = Test(name="John")
    t3: Test = Test(name="Sarah")
    assert t1 == t2
    assert t1 != t3

    assert hash(t1) == hash(t2)
    assert hash(t1) != hash(t3)


def test_decode_with_primitive_types() -> None:
    @immutable
    class Primitive(Classy):
        name: str
        age: int

    from_dict: Primitive = Primitive.from_dict({"name": "John", "age": 29})
    assert from_dict.name == "John"
    assert from_dict.age == 29


def test_default_with_empty_tuple() -> None:
    @immutable
    class EmptyTuples(Classy):
        tuples: tuple

    assert len(EmptyTuples.default().tuples) == 0


def test_jsonify_object_with_uuid() -> None:
    @immutable
    class HasId(Classy):
        id: UUID

    id: UUID = uuid4()

    assert HasId(id=id).json == f'{{"id": "{id}"}}'


def test_default_with_unsupported_types() -> None:
    @immutable
    class UnsupportedTypes(Classy):
        sets: set[str]

    with pytest.raises(TypeError):
        UnsupportedTypes.default()


def test_default_hash() -> None:
    @immutable
    class DefaultHash(Classy):
        name: str

    d1: DefaultHash = DefaultHash(name="John")
    with pytest.raises(NotImplementedError):
        hash(d1)
