    def _pad_or_backfill(
        self, *, method: FillnaOptions, limit: int | None = None, copy: bool = True
    ) -> Self:
        mask = self.isna()
        if mask.any():
            # (for now) when self.ndim == 2, we assume axis=0
            func = missing.get_fill_func(method, ndim=self.ndim)

            npvalues = self._ndarray.T
            if copy:
                npvalues = npvalues.copy()
            func(npvalues, limit=limit, mask=mask.T)
            npvalues = npvalues.T

            if copy:
                new_values = self._from_backing_data(npvalues)
            else:
                new_values = self

        else:
            if copy:
                new_values = self.copy()
            else:
                new_values = self
        return new_values
