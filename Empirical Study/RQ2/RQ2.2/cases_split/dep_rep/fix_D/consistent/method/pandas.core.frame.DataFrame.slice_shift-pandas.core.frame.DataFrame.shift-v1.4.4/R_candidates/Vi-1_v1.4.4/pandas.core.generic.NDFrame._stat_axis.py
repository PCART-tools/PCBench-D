    @property
    def _stat_axis(self) -> Index:
        return getattr(self, self._stat_axis_name)
