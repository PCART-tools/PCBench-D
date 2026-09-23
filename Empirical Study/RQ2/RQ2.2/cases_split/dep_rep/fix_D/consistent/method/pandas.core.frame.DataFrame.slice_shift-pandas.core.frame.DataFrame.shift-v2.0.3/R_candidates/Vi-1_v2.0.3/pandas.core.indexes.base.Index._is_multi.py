    @final
    @cache_readonly
    def _is_multi(self) -> bool:
        """
        Cached check equivalent to isinstance(self, MultiIndex)
        """
        return isinstance(self, ABCMultiIndex)
