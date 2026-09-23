    @minorformatter.setter
    def minorformatter(self, fmt):
        self._long_axis().set_minor_formatter(fmt)
        self._minorformatter = fmt
