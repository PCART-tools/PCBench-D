    def _pad_or_backfill(
        self, *, method: FillnaOptions, limit: int | None = None, copy: bool = True
    ) -> Self:
        # view as dt64 so we get treated as timelike in core.missing,
        #  similar to dtl._period_dispatch
        dta = self.view("M8[ns]")
        result = dta._pad_or_backfill(method=method, limit=limit, copy=copy)
        if copy:
            return cast("Self", result.view(self.dtype))
        else:
            return self
