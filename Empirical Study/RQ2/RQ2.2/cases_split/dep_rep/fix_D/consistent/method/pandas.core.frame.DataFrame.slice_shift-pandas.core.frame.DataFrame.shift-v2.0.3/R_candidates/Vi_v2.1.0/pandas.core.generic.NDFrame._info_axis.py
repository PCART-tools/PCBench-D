    @final
    @property
    def _info_axis(self) -> Index:
        return getattr(self, self._info_axis_name)
