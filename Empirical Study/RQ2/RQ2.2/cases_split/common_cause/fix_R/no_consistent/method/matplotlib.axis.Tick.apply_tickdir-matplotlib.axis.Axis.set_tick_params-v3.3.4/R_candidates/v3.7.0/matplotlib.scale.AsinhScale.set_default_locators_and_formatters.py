    def set_default_locators_and_formatters(self, axis):
        axis.set(major_locator=AsinhLocator(self.linear_width,
                                            base=self._base),
                 minor_locator=AsinhLocator(self.linear_width,
                                            base=self._base,
                                            subs=self._subs),
                 minor_formatter=NullFormatter())
        if self._base > 1:
            axis.set_major_formatter(LogFormatterSciNotation(self._base))
        else:
            axis.set_major_formatter('{x:.3g}'),
