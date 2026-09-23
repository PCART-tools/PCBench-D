    def __init__(self, *args, pad=0, **kwargs):
        """
        Parameters
        ----------
        pad : float, default: 0
            fraction of the axes height to put as padding.
        axes_class : matplotlib.axes.Axes

        *args
            Unpacked into axes_class() init for RGB
        **kwargs
            Unpacked into axes_class() init for RGB, R, G, B axes
        """
        axes_class = kwargs.pop("axes_class", self._defaultAxesClass)
        self.RGB = ax = axes_class(*args, **kwargs)
        ax.get_figure().add_axes(ax)
        self.R, self.G, self.B = make_rgb_axes(
            ax, pad=pad, axes_class=axes_class, **kwargs)
        # Set the line color and ticks for the axes.
        for ax1 in [self.RGB, self.R, self.G, self.B]:
            ax1.axis[:].line.set_color("w")
            ax1.axis[:].major_ticks.set_markeredgecolor("w")
