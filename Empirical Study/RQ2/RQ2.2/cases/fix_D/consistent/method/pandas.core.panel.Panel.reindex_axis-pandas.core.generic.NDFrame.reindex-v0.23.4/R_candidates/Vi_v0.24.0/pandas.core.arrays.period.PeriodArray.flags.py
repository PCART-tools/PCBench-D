    @property
    def flags(self):
        # TODO: remove
        # We need this since reduction.SeriesBinGrouper uses values.flags
        # Ideally, we wouldn't be passing objects down there in the first
        # place.
        return self._data.flags
