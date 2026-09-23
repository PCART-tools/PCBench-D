    def argmin(self, axis: int = 0, skipna: bool = True):  # type:ignore[override]
        # override base class by adding axis keyword
        validate_bool_kwarg(skipna, "skipna")
        if not skipna and self.isna().any():
            raise NotImplementedError
        return nargminmax(self, "argmin", axis=axis)
