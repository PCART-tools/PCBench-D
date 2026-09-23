    def axisinfo(self, unit, axis):
        """
        Return the `~matplotlib.units.AxisInfo` for *unit*.

        *unit* is a tzinfo instance or None.
        The *axis* argument is required but not used.
        """
        tz = unit

        majloc = AutoDateLocator(tz=tz,
                                 interval_multiples=self._interval_multiples)
        majfmt = AutoDateFormatter(majloc, tz=tz)
        datemin = datetime.date(1970, 1, 1)
        datemax = datetime.date(1970, 1, 2)

        return units.AxisInfo(majloc=majloc, majfmt=majfmt, label='',
                              default_limits=(datemin, datemax))
