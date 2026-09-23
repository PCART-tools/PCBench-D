    def axisinfo(self, unit, axis):
        # docstring inherited
        tz = unit
        majloc = AutoDateLocator(tz=tz,
                                 interval_multiples=self._interval_multiples)
        majfmt = ConciseDateFormatter(majloc, tz=tz, formats=self._formats,
                                      zero_formats=self._zero_formats,
                                      offset_formats=self._offset_formats,
                                      show_offset=self._show_offset)
        datemin = datetime.date(1970, 1, 1)
        datemax = datetime.date(1970, 1, 2)
        return units.AxisInfo(majloc=majloc, majfmt=majfmt, label='',
                              default_limits=(datemin, datemax))
