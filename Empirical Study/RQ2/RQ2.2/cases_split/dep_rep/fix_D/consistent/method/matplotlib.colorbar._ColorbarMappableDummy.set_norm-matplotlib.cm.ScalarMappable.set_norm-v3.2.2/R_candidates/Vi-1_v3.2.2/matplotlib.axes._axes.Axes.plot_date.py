    @_preprocess_data(replace_names=["x", "y"], label_namer="y")
    @docstring.dedent_interpd
    def plot_date(self, x, y, fmt='o', tz=None, xdate=True, ydate=False,
                  **kwargs):
        """
        Plot data that contains dates.

        Similar to `.plot`, this plots *y* vs. *x* as lines or markers.
        However, the axis labels are formatted as dates depending on *xdate*
        and *ydate*.

        Parameters
        ----------
        x, y : array-like
            The coordinates of the data points. If *xdate* or *ydate* is
            *True*, the respective values *x* or *y* are interpreted as
            :ref:`Matplotlib dates <date-format>`.

        fmt : str, optional
            The plot format string. For details, see the corresponding
            parameter in `.plot`.

        tz : timezone string or `tzinfo` or None
            The time zone to use in labeling dates. If *None*, defaults to
            :rc:`timezone`.

        xdate : bool, optional, default: True
            If *True*, the *x*-axis will be interpreted as Matplotlib dates.

        ydate : bool, optional, default: False
            If *True*, the *y*-axis will be interpreted as Matplotlib dates.


        Returns
        -------
        lines
            A list of `.Line2D` objects representing the plotted data.


        Other Parameters
        ----------------
        **kwargs
            Keyword arguments control the `.Line2D` properties:

            %(_Line2D_docstr)s

        See Also
        --------
        matplotlib.dates : Helper functions on dates.
        matplotlib.dates.date2num : Convert dates to num.
        matplotlib.dates.num2date : Convert num to dates.
        matplotlib.dates.drange : Create an equally spaced sequence of dates.

        Notes
        -----
        If you are using custom date tickers and formatters, it may be
        necessary to set the formatters/locators after the call to
        `.plot_date`. `.plot_date` will set the default tick locator to
        `.AutoDateLocator` (if the tick locator is not already set to a
        `.DateLocator` instance) and the default tick formatter to
        `.AutoDateFormatter` (if the tick formatter is not already set to a
        `.DateFormatter` instance).
        """
        if xdate:
            self.xaxis_date(tz)
        if ydate:
            self.yaxis_date(tz)

        ret = self.plot(x, y, fmt, **kwargs)

        self._request_autoscale_view()

        return ret
