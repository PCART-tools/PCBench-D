class TickHelper:
    axis = None

    def set_axis(self, axis):
        self.axis = axis

    def create_dummy_axis(self, **kwargs):
        if self.axis is None:
            self.axis = _DummyAxis(**kwargs)

    @_api.deprecated("3.5", alternative=".axis.set_view_interval")
    def set_view_interval(self, vmin, vmax):
        self.axis.set_view_interval(vmin, vmax)

    @_api.deprecated("3.5", alternative=".axis.set_data_interval")
    def set_data_interval(self, vmin, vmax):
        self.axis.set_data_interval(vmin, vmax)

    @_api.deprecated(
        "3.5",
        alternative=".axis.set_view_interval and .axis.set_data_interval")
    def set_bounds(self, vmin, vmax):
        self.set_view_interval(vmin, vmax)
        self.set_data_interval(vmin, vmax)
