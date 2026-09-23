    @classmethod
    def is_error(cls, value: int) -> bool:
        return 400 <= value <= 599
