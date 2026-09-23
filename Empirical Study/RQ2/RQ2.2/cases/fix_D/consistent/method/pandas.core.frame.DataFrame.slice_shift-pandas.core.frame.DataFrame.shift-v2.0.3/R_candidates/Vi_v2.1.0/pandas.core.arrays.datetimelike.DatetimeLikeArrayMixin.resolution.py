    @property  # NB: override with cache_readonly in immutable subclasses
    def resolution(self) -> str:
        """
        Returns day, hour, minute, second, millisecond or microsecond
        """
        # error: Item "None" of "Optional[Any]" has no attribute "attrname"
        return self._resolution_obj.attrname  # type: ignore[union-attr]
