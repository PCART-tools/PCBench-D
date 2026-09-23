    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # x in axes coords, y in data coords
        ax = self.axes
        self.tick1line.set(
            data=([0], [0]), transform=ax.get_yaxis_transform("tick1"))
        self.tick2line.set(
            data=([1], [0]), transform=ax.get_yaxis_transform("tick2"))
        self.gridline.set(
            data=([0, 1], [0, 0]), transform=ax.get_yaxis_transform("grid"))
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
