class _DummyAxis:
    __name__ = "dummy"

    # Once the deprecation elapses, replace dataLim and viewLim by plain
    # _view_interval and _data_interval private tuples.
    dataLim = _api.deprecate_privatize_attribute(
        "3.6", alternative="get_data_interval() and set_data_interval()")
    viewLim = _api.deprecate_privatize_attribute(
        "3.6", alternative="get_view_interval() and set_view_interval()")

    def __init__(self, minpos=0):
        self._dataLim = mtransforms.Bbox.unit()
        self._viewLim = mtransforms.Bbox.unit()
        self._minpos = minpos

    def get_view_interval(self):
        return self._viewLim.intervalx

    def set_view_interval(self, vmin, vmax):
        self._viewLim.intervalx = vmin, vmax

    def get_minpos(self):
        return self._minpos

    def get_data_interval(self):
        return self._dataLim.intervalx

    def set_data_interval(self, vmin, vmax):
        self._dataLim.intervalx = vmin, vmax

    def get_tick_space(self):
        # Just use the long-standing default of nbins==9
        return 9
