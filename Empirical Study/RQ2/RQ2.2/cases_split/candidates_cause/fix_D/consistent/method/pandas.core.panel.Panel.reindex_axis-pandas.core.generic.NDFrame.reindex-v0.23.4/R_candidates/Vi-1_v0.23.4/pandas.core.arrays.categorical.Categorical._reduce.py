    def _reduce(self, op, name, axis=0, skipna=True, numeric_only=None,
                filter_type=None, **kwds):
        """ perform the reduction type operation """
        func = getattr(self, name, None)
        if func is None:
            msg = 'Categorical cannot perform the operation {op}'
            raise TypeError(msg.format(op=name))
        return func(numeric_only=numeric_only, **kwds)
