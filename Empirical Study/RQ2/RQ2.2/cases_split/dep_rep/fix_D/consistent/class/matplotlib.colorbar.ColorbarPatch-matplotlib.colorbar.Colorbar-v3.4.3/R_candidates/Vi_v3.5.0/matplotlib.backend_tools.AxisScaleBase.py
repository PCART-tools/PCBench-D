class AxisScaleBase(ToolToggleBase):
    """Base Tool to toggle between linear and logarithmic."""

    def trigger(self, sender, event, data=None):
        if event.inaxes is None:
            return
        super().trigger(sender, event, data)

    def enable(self, event):
        self.set_scale(event.inaxes, 'log')
        self.figure.canvas.draw_idle()

    def disable(self, event):
        self.set_scale(event.inaxes, 'linear')
        self.figure.canvas.draw_idle()
