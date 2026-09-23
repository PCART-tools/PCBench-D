    @cache_readonly
    def size(self) -> int:
        """
        Return the len of myself.
        """
        return self._codes.size
