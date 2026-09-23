    def delete(self, loc) -> None:
        """
        Delete given loc(-s) from block in-place.
        """
        # Argument 1 to "delete" has incompatible type "Union[ndarray[Any, Any],
        # ExtensionArray]"; expected "Union[_SupportsArray[dtype[Any]],
        # Sequence[_SupportsArray[dtype[Any]]], Sequence[Sequence
        # [_SupportsArray[dtype[Any]]]], Sequence[Sequence[Sequence[
        # _SupportsArray[dtype[Any]]]]], Sequence[Sequence[Sequence[Sequence[
        # _SupportsArray[dtype[Any]]]]]]]"  [arg-type]
        self.values = np.delete(self.values, loc, 0)  # type: ignore[arg-type]
        self.mgr_locs = self._mgr_locs.delete(loc)
        try:
            self._cache.clear()
        except AttributeError:
            # _cache not yet initialized
            pass
