    def __contains__(self, key) -> bool:
        # https://github.com/pandas-dev/pandas/pull/51307#issuecomment-1426372604
        if isna(key) and key is not self.dtype.na_value:
            if self.dtype.kind == "f" and lib.is_float(key) and isna(key):
                return pc.any(pc.is_nan(self._data)).as_py()

            # e.g. date or timestamp types we do not allow None here to match pd.NA
            return False
            # TODO: maybe complex? object?

        return bool(super().__contains__(key))
