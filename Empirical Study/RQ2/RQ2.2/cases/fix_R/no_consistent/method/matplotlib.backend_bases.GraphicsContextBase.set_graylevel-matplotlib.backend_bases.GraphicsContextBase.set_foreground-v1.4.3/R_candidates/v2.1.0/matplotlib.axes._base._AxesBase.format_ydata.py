    def format_ydata(self, y):
        """
        Return y string formatted.  This function will use the
        :attr:`fmt_ydata` attribute if it is callable, else will fall
        back on the yaxis major formatter
        """
        try:
            return self.fmt_ydata(y)
        except TypeError:
            func = self.yaxis.get_major_formatter().format_data_short
            val = func(y)
            return val
