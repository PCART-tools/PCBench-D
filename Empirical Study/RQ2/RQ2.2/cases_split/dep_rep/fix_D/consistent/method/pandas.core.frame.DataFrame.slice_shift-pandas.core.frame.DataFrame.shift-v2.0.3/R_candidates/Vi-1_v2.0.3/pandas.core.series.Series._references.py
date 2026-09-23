    @property
    def _references(self) -> BlockValuesRefs | None:
        if isinstance(self._mgr, SingleArrayManager):
            return None
        return self._mgr._block.refs
