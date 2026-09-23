    @final
    def _get_level_names(self) -> Hashable | Sequence[Hashable]:
        """
        Return a name or list of names with None replaced by the level number.
        """
        if self._is_multi:
            return [
                level if name is None else name for level, name in enumerate(self.names)
            ]
        else:
            return 0 if self.name is None else self.name
