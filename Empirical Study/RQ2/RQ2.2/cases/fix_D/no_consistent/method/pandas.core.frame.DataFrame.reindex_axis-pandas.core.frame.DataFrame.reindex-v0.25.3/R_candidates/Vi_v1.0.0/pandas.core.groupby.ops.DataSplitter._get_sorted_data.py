    def _get_sorted_data(self) -> FrameOrSeries:
        return self.data.take(self.sort_idx, axis=self.axis)
