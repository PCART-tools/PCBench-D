    @formatter.setter
    def formatter(self, fmt):
        self._long_axis().set_major_formatter(fmt)
        self._formatter = fmt
