    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise errors.StrError()
        return v
