    def fetch_blocking(self) -> DataFrame:
        """Await the result synchronously."""
        return wrap_df(self._inner.fetch_blocking())
