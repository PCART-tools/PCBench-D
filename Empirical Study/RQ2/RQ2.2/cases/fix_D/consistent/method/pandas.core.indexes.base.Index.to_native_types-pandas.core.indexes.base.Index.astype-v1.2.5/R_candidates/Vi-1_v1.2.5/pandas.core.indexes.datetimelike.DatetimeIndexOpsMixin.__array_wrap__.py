    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc and other functions.
        """
        result = lib.item_from_zerodim(result)
        if is_bool_dtype(result) or lib.is_scalar(result):
            return result

        attrs = self._get_attributes_dict()
        if not is_period_dtype(self.dtype) and attrs["freq"]:
            # no need to infer if freq is None
            attrs["freq"] = "infer"
        return Index(result, **attrs)
