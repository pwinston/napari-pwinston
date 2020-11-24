class SomeClass:
    _list = []

    @classmethod
    def add_to_list(cls, value: int) -> None:
        cls._list.append(value)

