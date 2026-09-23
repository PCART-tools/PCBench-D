    def __array_wrap__(self, array, context=None):
        from pandas.core.dtypes.generic import ABCSparseSeries

        ufunc, inputs, _ = context
        inputs = tuple(x.values if isinstance(x, ABCSparseSeries) else x
                       for x in inputs)
        return self.__array_ufunc__(ufunc, '__call__', *inputs)
