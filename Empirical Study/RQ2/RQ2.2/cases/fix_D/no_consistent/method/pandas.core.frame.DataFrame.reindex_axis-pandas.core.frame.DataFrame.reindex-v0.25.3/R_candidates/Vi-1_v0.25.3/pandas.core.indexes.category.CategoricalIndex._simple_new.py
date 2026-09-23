    @classmethod
    def _simple_new(cls, values, name=None, dtype=None, **kwargs):
        result = object.__new__(cls)

        values = cls._create_categorical(values, dtype=dtype)
        result._data = values
        result.name = name
        for k, v in kwargs.items():
            setattr(result, k, v)

        result._reset_identity()
        return result
