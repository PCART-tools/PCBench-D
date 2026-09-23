    def _unbox_scalar(self, value, setitem: bool = False) -> np.datetime64:
        if not isinstance(value, self._scalar_type) and value is not NaT:
            raise ValueError("'value' should be a Timestamp.")
        self._check_compatible_with(value, setitem=setitem)
        return value.asm8
