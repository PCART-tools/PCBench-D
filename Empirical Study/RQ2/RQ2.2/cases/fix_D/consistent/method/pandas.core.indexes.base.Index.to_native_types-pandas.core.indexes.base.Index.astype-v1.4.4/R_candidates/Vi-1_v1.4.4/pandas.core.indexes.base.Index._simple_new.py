    @classmethod
    def _simple_new(cls: type[_IndexT], values, name: Hashable = None) -> _IndexT:
        """
        We require that we have a dtype compat for the values. If we are passed
        a non-dtype compat, then coerce using the constructor.

        Must be careful not to recurse.
        """
        assert isinstance(values, cls._data_cls), type(values)

        result = object.__new__(cls)
        result._data = values
        result._name = name
        result._cache = {}
        result._reset_identity()

        return result
