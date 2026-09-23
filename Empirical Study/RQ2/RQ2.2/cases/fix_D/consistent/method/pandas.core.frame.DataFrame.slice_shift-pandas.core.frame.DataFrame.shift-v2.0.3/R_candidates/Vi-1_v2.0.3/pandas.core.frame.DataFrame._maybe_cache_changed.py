    def _maybe_cache_changed(self, item, value: Series, inplace: bool) -> None:
        """
        The object has called back to us saying maybe it has changed.
        """
        loc = self._info_axis.get_loc(item)
        arraylike = value._values

        old = self._ixs(loc, axis=1)
        if old._values is value._values and inplace:
            # GH#46149 avoid making unnecessary copies/block-splitting
            return

        self._mgr.iset(loc, arraylike, inplace=inplace)
