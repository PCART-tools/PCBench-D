    def _validate_searchsorted_value(self, value):
        msg = "searchsorted requires compatible dtype or scalar"
        if not is_list_like(value):
            value = self._validate_scalar(value, msg, cast_str=True)
        else:
            # TODO: cast_str?  we accept it for scalar
            value = self._validate_listlike(value, "searchsorted")

        return self._unbox(value)
