    @property
    def agg_axis(self) -> Index:
        return self.obj._get_agg_axis(self.axis)
