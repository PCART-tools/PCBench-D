    def _pad_or_backfill(  # pylint: disable=useless-parent-delegation
        self, *, method: FillnaOptions, limit: int | None = None, copy: bool = True
    ) -> Self:
        # TODO(3.0): after EA.fillna 'method' deprecation is enforced, we can remove
        #  this method entirely.
        return super()._pad_or_backfill(method=method, limit=limit, copy=copy)
