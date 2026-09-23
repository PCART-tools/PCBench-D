    @classmethod
    def validate(cls, value: int) -> int:
        if cls.gt is not None and value <= cls.gt:
            raise ValueError(f'size less than minimum allowed: {cls.gt}')
        elif cls.lt is not None and value >= cls.lt:
            raise ValueError(f'size greater than maximum allowed: {cls.lt}')
        return value
