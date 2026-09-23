    @property  # NB: override with cache_readonly in immutable subclasses
    def resolution(self) -> str:
        """
        Returns day, hour, minute, second, millisecond or microsecond
        """
        return self._resolution_obj.attrname  # type: ignore
