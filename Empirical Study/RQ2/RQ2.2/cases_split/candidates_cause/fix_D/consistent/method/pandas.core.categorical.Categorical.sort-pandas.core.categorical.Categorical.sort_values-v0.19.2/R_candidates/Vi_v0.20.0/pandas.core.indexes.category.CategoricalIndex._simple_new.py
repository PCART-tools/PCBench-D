    @classmethod
    def _simple_new(cls, values, name=None, categories=None, ordered=None,
                    **kwargs):
        result = object.__new__(cls)

        values = cls._create_categorical(cls, values, categories, ordered)
        result._data = values
        result.name = name
        for k, v in compat.iteritems(kwargs):
            setattr(result, k, v)

        result._reset_identity()
        return result
