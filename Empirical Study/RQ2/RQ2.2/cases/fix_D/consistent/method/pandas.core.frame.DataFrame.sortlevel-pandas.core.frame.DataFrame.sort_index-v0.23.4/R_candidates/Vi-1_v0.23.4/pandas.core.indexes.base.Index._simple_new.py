    @classmethod
    def _simple_new(cls, values, name=None, dtype=None, **kwargs):
        """
        we require the we have a dtype compat for the values
        if we are passed a non-dtype compat, then coerce using the constructor

        Must be careful not to recurse.
        """
        if not hasattr(values, 'dtype'):
            if (values is None or not len(values)) and dtype is not None:
                values = np.empty(0, dtype=dtype)
            else:
                values = np.array(values, copy=False)
                if is_object_dtype(values):
                    values = cls(values, name=name, dtype=dtype,
                                 **kwargs)._ndarray_values

        result = object.__new__(cls)
        result._data = values
        result.name = name
        for k, v in compat.iteritems(kwargs):
            setattr(result, k, v)
        return result._reset_identity()
