    def format_ydata(self, y):
        """
        Return *y* formatted as a y-value.

        This function will use the `.fmt_ydata` attribute if it is not None,
        else will fall back on the yaxis major formatter.
        """
        return (self.fmt_ydata if self.fmt_ydata is not None
                else self.yaxis.get_major_formatter().format_data_short)(y)
