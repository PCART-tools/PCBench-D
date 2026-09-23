    def __new__(cls, value: int, phrase: str = "") -> "codes":
        obj = int.__new__(cls, value)  # type: ignore
        obj._value_ = value

        obj.phrase = phrase
        return obj
