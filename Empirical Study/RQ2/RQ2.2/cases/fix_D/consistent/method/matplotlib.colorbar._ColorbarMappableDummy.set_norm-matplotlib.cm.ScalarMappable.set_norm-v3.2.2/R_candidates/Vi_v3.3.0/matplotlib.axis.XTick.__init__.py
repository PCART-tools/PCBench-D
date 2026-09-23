    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # x in data coords, y in axes coords
        self.tick1line.set(
            xdata=[0], ydata=[0],
            transform=self.axes.get_xaxis_transform(which="tick1"),
            marker=self._tickmarkers[0],
        )
        self.tick2line.set(
            xdata=[0], ydata=[1],
            transform=self.axes.get_xaxis_transform(which="tick2"),
            marker=self._tickmarkers[1],
        )
        self.gridline.set(
            xdata=[0, 0], ydata=[0, 1],
            transform=self.axes.get_xaxis_transform(which="grid"),
        )
        # the y loc is 3 points below the min of y axis
        trans, va, ha = self._get_text1_transform()
        self.label1.set(
            x=0, y=0,
            verticalalignment=va, horizontalalignment=ha, transform=trans,
        )
        trans, va, ha = self._get_text2_transform()
        self.label2.set(
            x=0, y=1,
            verticalalignment=va, horizontalalignment=ha, transform=trans,
        )
