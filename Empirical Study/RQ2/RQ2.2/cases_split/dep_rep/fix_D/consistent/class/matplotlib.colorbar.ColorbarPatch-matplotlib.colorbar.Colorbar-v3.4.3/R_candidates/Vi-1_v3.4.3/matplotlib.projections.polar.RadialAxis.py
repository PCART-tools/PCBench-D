class RadialAxis(maxis.YAxis):
    """
    A radial Axis.

    This overrides certain properties of a `.YAxis` to provide special-casing
    for a radial axis.
    """
    __name__ = 'radialaxis'
    axis_name = 'radius'  #: Read-only name identifying the axis.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sticky_edges.y.append(0)

    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return RadialTick(self.axes, 0, major=major, **tick_kw)

    def _wrap_locator_formatter(self):
        self.set_major_locator(RadialLocator(self.get_major_locator(),
                                             self.axes))
        self.isDefault_majloc = True

    def clear(self):
        super().clear()
        self.set_ticks_position('none')
        self._wrap_locator_formatter()

    @_api.deprecated("3.4", alternative="RadialAxis.clear()")
    def cla(self):
        self.clear()

    def _set_scale(self, value, **kwargs):
        super()._set_scale(value, **kwargs)
        self._wrap_locator_formatter()
