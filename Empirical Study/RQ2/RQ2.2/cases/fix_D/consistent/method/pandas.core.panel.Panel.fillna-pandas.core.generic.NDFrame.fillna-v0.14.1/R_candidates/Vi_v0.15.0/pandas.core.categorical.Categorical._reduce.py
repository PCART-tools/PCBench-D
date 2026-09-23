    def _reduce(self, op, axis=0, skipna=True, numeric_only=None,
                filter_type=None, name=None, **kwds):
        """ perform the reduction type operation """
        func = getattr(self,name,None)
        if func is None:
            raise TypeError("Categorical cannot perform the operation {op}".format(op=name))
        return func(numeric_only=numeric_only, **kwds)
