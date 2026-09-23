    @_api.deprecated(
        "3.5",
        alternative=".axis.set_view_interval and .axis.set_data_interval")
    def set_bounds(self, vmin, vmax):
        self.set_view_interval(vmin, vmax)
        self.set_data_interval(vmin, vmax)
