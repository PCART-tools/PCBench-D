    @_preprocess_data(replace_all_args=True, label_namer=None)
    def stem(self, *args, **kwargs):
        """
        Create a stem plot.

        Call signatures::

          stem(y, linefmt='b-', markerfmt='bo', basefmt='r-')
          stem(x, y, linefmt='b-', markerfmt='bo', basefmt='r-')

        A stem plot plots vertical lines (using *linefmt*) at each *x*
        location from the baseline to *y*, and places a marker there
        using *markerfmt*.  A horizontal line at 0 is plotted using
        *basefmt*.

        If no *x* values are provided, the default is (0, 1, ..., len(y) - 1)

        Return value is a tuple (*markerline*, *stemlines*,
        *baseline*). See :class:`~matplotlib.container.StemContainer`

        .. seealso::
            This
            `document <http://www.mathworks.com/help/techdoc/ref/stem.html>`_
            for details.

        """
        remember_hold = self._hold
        if not self._hold:
            self.cla()
        self._hold = True

        # Assume there's at least one data array
        y = np.asarray(args[0])
        args = args[1:]

        # Try a second one
        try:
            second = np.asarray(args[0], dtype=float)
            x, y = y, second
            args = args[1:]
        except (IndexError, ValueError):
            # The second array doesn't make sense, or it doesn't exist
            second = np.arange(len(y))
            x = second

        # Popping some defaults
        try:
            linefmt = kwargs['linefmt']
        except KeyError:
            try:
                linefmt = args[0]
            except IndexError:
                linecolor = 'C0'
                linemarker = 'None'
                linestyle = '-'
            else:
                linestyle, linemarker, linecolor = \
                    _process_plot_format(linefmt)
        else:
            linestyle, linemarker, linecolor = _process_plot_format(linefmt)
        try:
            markerfmt = kwargs['markerfmt']
        except KeyError:
            try:
                markerfmt = args[1]
            except IndexError:
                markercolor = 'C0'
                markermarker = 'o'
                markerstyle = 'None'
            else:
                markerstyle, markermarker, markercolor = \
                    _process_plot_format(markerfmt)
        else:
            markerstyle, markermarker, markercolor = \
                _process_plot_format(markerfmt)
        try:
            basefmt = kwargs['basefmt']
        except KeyError:
            try:
                basefmt = args[2]
            except IndexError:
                if rcParams['_internal.classic_mode']:
                    basecolor = 'C2'
                else:
                    basecolor = 'C3'
                basemarker = 'None'
                basestyle = '-'
            else:
                basestyle, basemarker, basecolor = \
                    _process_plot_format(basefmt)
        else:
            basestyle, basemarker, basecolor = _process_plot_format(basefmt)

        bottom = kwargs.pop('bottom', None)
        label = kwargs.pop('label', None)

        markerline, = self.plot(x, y, color=markercolor, linestyle=markerstyle,
                                marker=markermarker, label="_nolegend_")

        if bottom is None:
            bottom = 0

        stemlines = []
        for thisx, thisy in zip(x, y):
            l, = self.plot([thisx, thisx], [bottom, thisy],
                           color=linecolor, linestyle=linestyle,
                           marker=linemarker, label="_nolegend_")
            stemlines.append(l)

        baseline, = self.plot([np.min(x), np.max(x)], [bottom, bottom],
                              color=basecolor, linestyle=basestyle,
                              marker=basemarker, label="_nolegend_")

        self._hold = remember_hold

        stem_container = StemContainer((markerline, stemlines, baseline),
                                       label=label)
        self.add_container(stem_container)

        return stem_container
