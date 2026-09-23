    def sharey(self, other):
        """
        Share the y-axis with *other*.

        This is equivalent to passing ``sharey=other`` when constructing the
        axes, and cannot be used if the y-axis is already being shared with
        another axes.
        """
        cbook._check_isinstance(_AxesBase, other=other)
        if self._sharey is not None and other is not self._sharey:
            raise ValueError("y-axis is already shared")
        self._shared_y_axes.join(self, other)
        self._sharey = other
        self.yaxis.major = other.yaxis.major  # Ticker instances holding
        self.yaxis.minor = other.yaxis.minor  # locator and formatter.
        y0, y1 = other.get_ylim()
        self.set_ylim(y0, y1, emit=False, auto=other.get_autoscaley_on())
        self.yaxis._scale = other.yaxis._scale
