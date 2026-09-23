    def _unbox_scalar(self, value, setitem: bool = False) -> np.timedelta64:
        if not isinstance(value, self._scalar_type) and value is not NaT:
            raise ValueError("'value' should be a Timedelta.")
        self._check_compatible_with(value, setitem=setitem)
        return np.timedelta64(value.value, "ns")
