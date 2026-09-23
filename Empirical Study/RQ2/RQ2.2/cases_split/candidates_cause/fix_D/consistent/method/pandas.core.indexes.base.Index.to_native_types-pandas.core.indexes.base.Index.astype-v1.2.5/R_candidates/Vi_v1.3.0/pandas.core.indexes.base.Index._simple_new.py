    @classmethod
    def _simple_new(cls: type[_IndexT], values, name: Hashable = None) -> _IndexT:
        """
        We require that we have a dtype compat for the values. If we are passed
        a non-dtype compat, then coerce using the constructor.

        Must be careful not to recurse.
        """
        assert isinstance(values, np.ndarray), type(values)

        result = object.__new__(cls)
        result._data = values
        # _index_data is a (temporary?) fix to ensure that the direct data
        # manipulation we do in `_libs/reduction.pyx` continues to work.
        # We need access to the actual ndarray, since we're messing with
        # data buffers and strides.
        result._index_data = values
        result._name = name
        result._cache = {}
        result._reset_identity()

        return result
