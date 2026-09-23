    @classmethod
    def _simple_new(cls, values, name=None, dtype=None):
        result = object.__new__(cls)

        values = cls._create_categorical(values, dtype=dtype)
        result._data = values
        result.name = name

        result._reset_identity()
        result._no_setting_name = False
        return result
