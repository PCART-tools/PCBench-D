    @property
    def _hasna(self) -> bool:
        # GH#22680
        """
        Equivalent to `self.isna().any()`.

        Some ExtensionArray subclasses may be able to optimize this check.
        """
        return bool(self.isna().any())
