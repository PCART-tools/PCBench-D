    def argmax(self, axis: AxisInt = 0, skipna: bool = True):  # type: ignore[override]
        # override base class by adding axis keyword
        validate_bool_kwarg(skipna, "skipna")
        if not skipna and self._hasna:
            raise NotImplementedError
        return nargminmax(self, "argmax", axis=axis)
