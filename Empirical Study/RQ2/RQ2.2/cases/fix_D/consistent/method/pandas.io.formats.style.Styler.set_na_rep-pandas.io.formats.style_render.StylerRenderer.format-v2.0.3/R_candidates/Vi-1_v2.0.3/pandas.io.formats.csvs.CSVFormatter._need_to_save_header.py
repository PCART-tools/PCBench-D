    @property
    def _need_to_save_header(self) -> bool:
        return bool(self._has_aliases or self.header)
