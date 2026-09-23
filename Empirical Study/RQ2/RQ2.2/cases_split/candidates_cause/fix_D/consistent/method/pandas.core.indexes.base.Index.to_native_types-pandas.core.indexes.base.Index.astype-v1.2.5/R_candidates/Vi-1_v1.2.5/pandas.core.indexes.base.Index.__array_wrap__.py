    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc and other functions.
        """
        result = lib.item_from_zerodim(result)
        if is_bool_dtype(result) or lib.is_scalar(result) or np.ndim(result) > 1:
            return result

        attrs = self._get_attributes_dict()
        return Index(result, **attrs)
