    def _unbox_scalar(self, value: Union[Period, NaTType]) -> int:
        if value is NaT:
            return value.value
        elif isinstance(value, self._scalar_type):
            if not isna(value):
                self._check_compatible_with(value)
            return value.ordinal
        else:
            raise ValueError(
                "'value' should be a Period. Got '{val}' instead.".format(val=value)
            )
