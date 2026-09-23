class _DummyAxis:
    __name__ = "dummy"

    def __init__(self, minpos=0):
        self.dataLim = mtransforms.Bbox.unit()
        self.viewLim = mtransforms.Bbox.unit()
        self._minpos = minpos

    def get_view_interval(self):
        return self.viewLim.intervalx

    def set_view_interval(self, vmin, vmax):
        self.viewLim.intervalx = vmin, vmax

    def get_minpos(self):
        return self._minpos

    def get_data_interval(self):
        return self.dataLim.intervalx

    def set_data_interval(self, vmin, vmax):
        self.dataLim.intervalx = vmin, vmax

    def get_tick_space(self):
        # Just use the long-standing default of nbins==9
        return 9
