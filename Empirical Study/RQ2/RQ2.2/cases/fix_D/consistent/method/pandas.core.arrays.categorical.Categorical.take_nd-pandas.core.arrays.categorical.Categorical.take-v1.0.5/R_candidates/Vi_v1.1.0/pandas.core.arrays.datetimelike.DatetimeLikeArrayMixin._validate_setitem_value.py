    def _validate_setitem_value(self, value):
        msg = (
            f"'value' should be a '{self._scalar_type.__name__}', 'NaT', "
            f"or array of those. Got '{type(value).__name__}' instead."
        )
        if is_list_like(value):
            value = self._validate_listlike(value, "setitem", cast_str=True)
        else:
            # TODO: cast_str for consistency?
            value = self._validate_scalar(value, msg, cast_str=False)

        self._check_compatible_with(value, setitem=True)
        return self._unbox(value)
