    @final
    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc and other functions e.g. np.split.
        """
        result = lib.item_from_zerodim(result)
        if (not isinstance(result, Index) and is_bool_dtype(result.dtype)) or np.ndim(
            result
        ) > 1:
            # exclude Index to avoid warning from is_bool_dtype deprecation;
            #  in the Index case it doesn't matter which path we go down.
            # reached in plotting tests with e.g. np.nonzero(index)
            return result

        return Index(result, name=self.name)
