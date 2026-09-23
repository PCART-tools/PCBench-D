class ToolXScale(AxisScaleBase):
    """Tool to toggle between linear and logarithmic scales on the X axis."""

    description = 'Toggle scale X axis'
    default_keymap = property(lambda self: mpl.rcParams['keymap.xscale'])

    def set_scale(self, ax, scale):
        ax.set_xscale(scale)
