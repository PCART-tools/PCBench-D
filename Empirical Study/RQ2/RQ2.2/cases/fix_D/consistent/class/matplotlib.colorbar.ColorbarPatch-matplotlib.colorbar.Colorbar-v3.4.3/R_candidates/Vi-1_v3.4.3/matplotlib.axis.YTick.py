class YTick(Tick):
    """
    Contains all the Artists needed to make a Y tick - the tick line,
    the label text and the grid line
    """
    __name__ = 'ytick'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # x in axes coords, y in data coords
        self.tick1line.set(
            xdata=[0], ydata=[0],
            transform=self.axes.get_yaxis_transform(which="tick1"),
            marker=self._tickmarkers[0],
        )
        self.tick2line.set(
            xdata=[1], ydata=[0],
            transform=self.axes.get_yaxis_transform(which="tick2"),
            marker=self._tickmarkers[1],
        )
        self.gridline.set(
            xdata=[0, 1], ydata=[0, 0],
            transform=self.axes.get_yaxis_transform(which="grid"),
        )
        # the y loc is 3 points below the min of y axis
        trans, va, ha = self._get_text1_transform()
        self.label1.set(
            x=0, y=0,
            verticalalignment=va, horizontalalignment=ha, transform=trans,
        )
        trans, va, ha = self._get_text2_transform()
        self.label2.set(
            x=1, y=0,
            verticalalignment=va, horizontalalignment=ha, transform=trans,
        )

    def _get_text1_transform(self):
        return self.axes.get_yaxis_text1_transform(self._pad)

    def _get_text2_transform(self):
        return self.axes.get_yaxis_text2_transform(self._pad)

    def apply_tickdir(self, tickdir):
        # docstring inherited
        super().apply_tickdir(tickdir)
        self._tickmarkers = {
            'out': (mlines.TICKLEFT, mlines.TICKRIGHT),
            'in': (mlines.TICKRIGHT, mlines.TICKLEFT),
            'inout': ('_', '_'),
        }[self._tickdir]
        self.stale = True

    def update_position(self, loc):
        """Set the location of tick in data coords with scalar *loc*."""
        self.tick1line.set_ydata((loc,))
        self.tick2line.set_ydata((loc,))
        self.gridline.set_ydata((loc,))
        self.label1.set_y(loc)
        self.label2.set_y(loc)
        self._loc = loc
        self.stale = True

    def get_view_interval(self):
        # docstring inherited
        return self.axes.viewLim.intervaly
