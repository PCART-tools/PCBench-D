    def _validate_searchsorted_value(self, value):
        if not is_list_like(value):
            return self._validate_scalar(value, allow_listlike=True, setitem=False)
        else:
            value = self._validate_listlike(value)

        return self._unbox(value)
