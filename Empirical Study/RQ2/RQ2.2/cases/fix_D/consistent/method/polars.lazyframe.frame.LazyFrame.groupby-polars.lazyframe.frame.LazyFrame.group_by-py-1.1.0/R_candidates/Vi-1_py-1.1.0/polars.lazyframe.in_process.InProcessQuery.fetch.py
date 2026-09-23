    def fetch(self) -> DataFrame | None:
        """
        Fetch the result.

        If it is ready, a materialized DataFrame is returned.
        If it is not ready it will return `None`.
        """
        out = self._inner.fetch()
        if out is not None:
            return wrap_df(out)
        else:
            return None
