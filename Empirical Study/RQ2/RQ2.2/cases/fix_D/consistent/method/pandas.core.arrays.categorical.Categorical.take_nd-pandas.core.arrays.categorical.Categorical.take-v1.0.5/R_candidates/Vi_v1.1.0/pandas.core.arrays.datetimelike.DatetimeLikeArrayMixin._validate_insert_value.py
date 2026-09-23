    def _validate_insert_value(self, value):
        msg = f"cannot insert {type(self).__name__} with incompatible label"
        value = self._validate_scalar(value, msg, cast_str=False)

        self._check_compatible_with(value, setitem=True)
        # TODO: if we dont have compat, should we raise or astype(object)?
        #  PeriodIndex does astype(object)
        return value
