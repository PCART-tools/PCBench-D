    @classmethod
    def _from_ordinals(cls, values, name=None, freq=None, **kwargs):
        """
        Values should be int ordinals
        `__new__` & `_simple_new` cooerce to ordinals and call this method
        """

        values = np.array(values, dtype='int64', copy=False)

        result = object.__new__(cls)
        result._data = values
        result.name = name
        if freq is None:
            raise ValueError('freq is not specified and cannot be inferred')
        result._freq = Period._maybe_convert_freq(freq)
        result._reset_identity()
        return result
