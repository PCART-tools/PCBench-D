    @property
    def na_value(self) -> libmissing.NAType | float:  # type: ignore[override]
        if self.storage == "pyarrow_numpy":
            return np.nan
        else:
            return libmissing.NA
