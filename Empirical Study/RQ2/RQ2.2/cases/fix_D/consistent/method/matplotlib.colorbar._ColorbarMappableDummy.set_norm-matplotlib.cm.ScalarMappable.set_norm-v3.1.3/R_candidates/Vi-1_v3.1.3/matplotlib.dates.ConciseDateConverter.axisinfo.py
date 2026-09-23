    def axisinfo(self, unit, axis):
        """
        Return the :class:`~matplotlib.units.AxisInfo` for *unit*.

        *unit* is a tzinfo instance or None.
        The *axis* argument is required but not used.
        """
        tz = unit

        majloc = AutoDateLocator(tz=tz)
        majfmt = ConciseDateFormatter(majloc, tz=tz, formats=self._formats,
                                      zero_formats=self._zero_formats,
                                      offset_formats=self._offset_formats,
                                      show_offset=self._show_offset)
        datemin = datetime.date(2000, 1, 1)
        datemax = datetime.date(2010, 1, 1)

        return units.AxisInfo(majloc=majloc, majfmt=majfmt, label='',
                              default_limits=(datemin, datemax))
