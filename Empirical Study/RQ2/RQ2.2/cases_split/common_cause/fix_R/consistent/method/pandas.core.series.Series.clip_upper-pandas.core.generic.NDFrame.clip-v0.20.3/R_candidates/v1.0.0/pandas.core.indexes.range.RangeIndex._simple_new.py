    @classmethod
    def _simple_new(cls, values, name=None, dtype=None):
        result = object.__new__(cls)

        # handle passed None, non-integers
        if values is None:
            # empty
            values = range(0, 0, 1)
        elif not isinstance(values, range):
            return Index(values, dtype=dtype, name=name)

        result._range = values
        result.name = name

        result._reset_identity()
        return result
