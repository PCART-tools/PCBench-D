    @classmethod
    def validate(cls, value: str) -> str:
        if value is None:
            raise TypeError('None is not an allow value')

        v_len = len(value)
        if cls.min_length is not None and v_len < cls.min_length:
            raise ValueError(f'length less than minimum allowed: {cls.min_length}')

        if cls.curtail_length:
            if v_len > cls.curtail_length:
                value = value[:cls.curtail_length]
        elif cls.max_length is not None and v_len > cls.max_length:
            raise ValueError(f'length greater than maximum allowed: {cls.max_length}')

        if cls.regex:
            if not cls.regex.match(value):
                raise ValueError(f'string does not match regex "{cls.regex.pattern}"')
        return value
