    @property
    def shape(self) -> Shape:
        return tuple(len(ax) for ax in self.axes)
