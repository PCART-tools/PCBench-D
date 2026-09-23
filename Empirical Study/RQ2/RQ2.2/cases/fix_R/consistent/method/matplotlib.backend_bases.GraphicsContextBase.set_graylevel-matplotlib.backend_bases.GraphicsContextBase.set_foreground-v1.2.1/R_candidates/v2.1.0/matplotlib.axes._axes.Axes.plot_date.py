    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    @docstring.dedent_interpd
    def plot_date(self, x, y, fmt='o', tz=None, xdate=True, ydate=False,
                  **kwargs):
        """
        A plot with data that contains dates.

        Similar to the :func:`~matplotlib.pyplot.plot` command, except
        the *x* or *y* (or both) data is considered to be dates, and the
        axis is labeled accordingly.

        *x* and/or *y* can be a sequence of dates represented as float
        days since 0001-01-01 UTC.

        Note if you are using custom date tickers and formatters, it
        may be necessary to set the formatters/locators after the call
        to :meth:`plot_date` since :meth:`plot_date` will set the
        default tick locator to
        :class:`matplotlib.dates.AutoDateLocator` (if the tick
        locator is not already set to a
        :class:`matplotlib.dates.DateLocator` instance) and the
        default tick formatter to
        :class:`matplotlib.dates.AutoDateFormatter` (if the tick
        formatter is not already set to a
        :class:`matplotlib.dates.DateFormatter` instance).


        Parameters
        ----------
        fmt : string
            The plot format string.

        tz : [ *None* | timezone string | :class:`tzinfo` instance]
            The time zone to use in labeling dates. If *None*, defaults to rc
            value.

        xdate : boolean
            If *True*, the *x*-axis will be labeled with dates.

        ydate : boolean
            If *True*, the *y*-axis will be labeled with dates.


        Returns
        -------
        lines


        See Also
        --------
        matplotlib.dates : helper functions on dates
        matplotlib.dates.date2num : how to convert dates to num
        matplotlib.dates.num2date : how to convert num to dates
        matplotlib.dates.drange : how floating point dates

        Other Parameters
        ----------------
        **kwargs :
            Keyword arguments control the :class:`~matplotlib.lines.Line2D`
            properties:

            %(Line2D)s

        """

        if not self._hold:
            self.cla()

        if xdate:
            self.xaxis_date(tz)
        if ydate:
            self.yaxis_date(tz)

        ret = self.plot(x, y, fmt, **kwargs)

        self.autoscale_view()

        return ret
