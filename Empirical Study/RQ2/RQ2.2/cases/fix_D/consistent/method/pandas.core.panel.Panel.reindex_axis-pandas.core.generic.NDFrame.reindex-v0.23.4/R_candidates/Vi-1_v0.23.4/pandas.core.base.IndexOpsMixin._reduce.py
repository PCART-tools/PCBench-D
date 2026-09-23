    def _reduce(self, op, name, axis=0, skipna=True, numeric_only=None,
                filter_type=None, **kwds):
        """ perform the reduction type operation if we can """
        func = getattr(self, name, None)
        if func is None:
            raise TypeError("{klass} cannot perform the operation {op}".format(
                            klass=self.__class__.__name__, op=name))
        return func(**kwds)
