    def sharex(self, other):
        """
        Share the x-axis with *other*.

        This is equivalent to passing ``sharex=other`` when constructing the
        axes, and cannot be used if the x-axis is already being shared with
        another axes.
        """
        cbook._check_isinstance(_AxesBase, other=other)
        if self._sharex is not None and other is not self._sharex:
            raise ValueError("x-axis is already shared")
        self._shared_x_axes.join(self, other)
        self._sharex = other
        self.xaxis.major = other.xaxis.major  # Ticker instances holding
        self.xaxis.minor = other.xaxis.minor  # locator and formatter.
        x0, x1 = other.get_xlim()
        self.set_xlim(x0, x1, emit=False, auto=other.get_autoscalex_on())
        self.xaxis._scale = other.xaxis._scale
