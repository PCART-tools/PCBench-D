    def any(self, *, axis: int | None = None, skipna: bool = True) -> bool:
        # GH#34479 discussion of desired behavior long-term
        return nanops.nanany(self._ndarray, axis=axis, skipna=skipna, mask=self.isna())
