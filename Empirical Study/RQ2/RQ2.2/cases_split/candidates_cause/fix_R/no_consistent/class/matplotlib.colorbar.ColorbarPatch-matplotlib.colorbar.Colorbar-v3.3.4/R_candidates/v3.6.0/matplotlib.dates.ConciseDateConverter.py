class ConciseDateConverter(DateConverter):
    # docstring inherited

    def __init__(self, formats=None, zero_formats=None, offset_formats=None,
                 show_offset=True, *, interval_multiples=True):
        self._formats = formats
        self._zero_formats = zero_formats
        self._offset_formats = offset_formats
        self._show_offset = show_offset
        self._interval_multiples = interval_multiples
        super().__init__()

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
