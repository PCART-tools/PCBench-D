    def _reduce(self, op, axis=0, skipna=True, numeric_only=None,
                filter_type=None, **kwds):
        """ perform a reduction operation """
        return op(_values_from_object(self), skipna=skipna, **kwds)
