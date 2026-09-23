    def _pad_or_backfill(  # pylint: disable=useless-parent-delegation
        self, *, method: FillnaOptions, limit: int | None = None, copy: bool = True
    ) -> Self:
        # TODO(3.0): We can remove this method once deprecation for fillna method
        #  keyword is enforced.
        return super()._pad_or_backfill(method=method, limit=limit, copy=copy)
