    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc
        """
        if is_bool_dtype(result):
            return result

        attrs = self._get_attributes_dict()
        attrs = self._maybe_update_attributes(attrs)
        return Index(result, **attrs)
