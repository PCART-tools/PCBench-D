    def cancel(self) -> None:
        """Cancel the query at earliest convenience."""
        self._inner.cancel()
