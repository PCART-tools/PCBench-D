    @cache_readonly
    def sorted_data(self) -> NDFrameT:
        return self.data.take(self._sort_idx, axis=self.axis)
