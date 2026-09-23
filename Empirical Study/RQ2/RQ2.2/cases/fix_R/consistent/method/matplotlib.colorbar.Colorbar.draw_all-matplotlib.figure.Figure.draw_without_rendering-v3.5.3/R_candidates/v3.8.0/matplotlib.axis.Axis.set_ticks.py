    def set_ticks(self, ticks, labels=None, *, minor=False, **kwargs):
        """
        Set this Axis' tick locations and optionally tick labels.

        If necessary, the view limits of the Axis are expanded so that all
        given ticks are visible.

        Parameters
        ----------
        ticks : 1D array-like
            Array of tick locations.  The axis `.Locator` is replaced by a
            `~.ticker.FixedLocator`.

            The values may be either floats or in axis units.

            Pass an empty list to remove all ticks::

                set_ticks([])

            Some tick formatters will not label arbitrary tick positions;
            e.g. log formatters only label decade ticks by default. In
            such a case you can set a formatter explicitly on the axis
            using `.Axis.set_major_formatter` or provide formatted
            *labels* yourself.
        labels : list of str, optional
            Tick labels for each location in *ticks*. *labels* must be of the same
            length as *ticks*. If not set, the labels are generate using the axis
            tick `.Formatter`.
        minor : bool, default: False
            If ``False``, set the major ticks; if ``True``, the minor ticks.
        **kwargs
            `.Text` properties for the labels. Using these is only allowed if
            you pass *labels*. In other cases, please use `~.Axes.tick_params`.

        Notes
        -----
        The mandatory expansion of the view limits is an intentional design
        choice to prevent the surprise of a non-visible tick. If you need
        other limits, you should set the limits explicitly after setting the
        ticks.
        """
        if labels is None and kwargs:
            first_key = next(iter(kwargs))
            raise ValueError(
                f"Incorrect use of keyword argument {first_key!r}. Keyword arguments "
                "other than 'minor' modify the text labels and can only be used if "
                "'labels' are passed as well.")
        result = self._set_tick_locations(ticks, minor=minor)
        if labels is not None:
            self.set_ticklabels(labels, minor=minor, **kwargs)
        return result
