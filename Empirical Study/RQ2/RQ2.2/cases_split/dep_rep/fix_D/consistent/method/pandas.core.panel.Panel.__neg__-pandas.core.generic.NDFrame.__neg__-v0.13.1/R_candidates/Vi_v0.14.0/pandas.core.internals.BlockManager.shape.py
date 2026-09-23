    @property
    def shape(self):
        return tuple(len(ax) for ax in self.axes)
