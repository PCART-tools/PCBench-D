class ToolYScale(AxisScaleBase):
    """Tool to toggle between linear and logarithmic scales on the Y axis."""

    description = 'Toggle scale Y axis'
    default_keymap = mpl.rcParams['keymap.yscale']

    def set_scale(self, ax, scale):
        ax.set_yscale(scale)
