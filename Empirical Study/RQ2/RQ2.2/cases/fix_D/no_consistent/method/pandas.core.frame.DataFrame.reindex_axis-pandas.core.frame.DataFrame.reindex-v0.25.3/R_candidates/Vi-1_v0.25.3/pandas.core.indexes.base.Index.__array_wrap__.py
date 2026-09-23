    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc.
        """
        result = lib.item_from_zerodim(result)
        if is_bool_dtype(result) or lib.is_scalar(result):
            return result

        attrs = self._get_attributes_dict()
        attrs = self._maybe_update_attributes(attrs)
        return Index(result, **attrs)
