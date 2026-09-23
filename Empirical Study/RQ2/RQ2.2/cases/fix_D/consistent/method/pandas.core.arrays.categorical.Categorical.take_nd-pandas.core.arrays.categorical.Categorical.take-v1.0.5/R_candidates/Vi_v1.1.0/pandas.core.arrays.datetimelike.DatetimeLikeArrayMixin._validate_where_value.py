    def _validate_where_value(self, other):
        msg = f"Where requires matching dtype, not {type(other)}"
        if not is_list_like(other):
            other = self._validate_scalar(other, msg)
        else:
            other = self._validate_listlike(other, "where")
            self._check_compatible_with(other, setitem=True)

        self._check_compatible_with(other, setitem=True)
        return self._unbox(other)
