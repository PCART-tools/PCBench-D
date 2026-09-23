    def get_series_dict(self):
        # For DataFrame
        return _blocks_to_series_dict(self.blocks, self.axes[1])
