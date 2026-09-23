    @_api.deprecated("3.5", alternative="`.Axis.set_data_interval`")
    def set_data_interval(self, vmin, vmax):
        self.axis.set_data_interval(vmin, vmax)
