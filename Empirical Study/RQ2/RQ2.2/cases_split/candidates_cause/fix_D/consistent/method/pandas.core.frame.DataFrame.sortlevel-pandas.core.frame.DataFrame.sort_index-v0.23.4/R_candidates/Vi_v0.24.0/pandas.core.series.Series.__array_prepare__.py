    def __array_prepare__(self, result, context=None):
        """
        Gets called prior to a ufunc.
        """

        # nice error message for non-ufunc types
        if (context is not None and
                (not isinstance(self._values, (np.ndarray, ExtensionArray))
                 or isinstance(self._values, Categorical))):
            obj = context[1][0]
            raise TypeError("{obj} with dtype {dtype} cannot perform "
                            "the numpy op {op}".format(
                                obj=type(obj).__name__,
                                dtype=getattr(obj, 'dtype', None),
                                op=context[0].__name__))
        return result
