    @_preprocess_data(replace_names=["x", "y"],
                      positional_parameter_names=_plot_args_replacer,
                      label_namer=None)
    @docstring.dedent_interpd
    def plot(self, *args, **kwargs):
        """
        Plot lines and/or markers to the
        :class:`~matplotlib.axes.Axes`.  *args* is a variable length
        argument, allowing for multiple *x*, *y* pairs with an
        optional format string.  For example, each of the following is
        legal::

            plot(x, y)        # plot x and y using default line style and color
            plot(x, y, 'bo')  # plot x and y using blue circle markers
            plot(y)           # plot y using x as index array 0..N-1
            plot(y, 'r+')     # ditto, but with red plusses

        If *x* and/or *y* is 2-dimensional, then the corresponding columns
        will be plotted.

        If used with labeled data, make sure that the color spec is not
        included as an element in data, as otherwise the last case
        ``plot("v","r", data={"v":..., "r":...)``
        can be interpreted as the first case which would do ``plot(v, r)``
        using the default line style and color.

        If not used with labeled data (i.e., without a data argument),
        an arbitrary number of *x*, *y*, *fmt* groups can be specified, as in::

            a.plot(x1, y1, 'g^', x2, y2, 'g-')

        Return value is a list of lines that were added.

        By default, each line is assigned a different style specified by a
        'style cycle'.  To change this behavior, you can edit the
        axes.prop_cycle rcParam.

        The following format string characters are accepted to control
        the line style or marker:

        ================    ===============================
        character           description
        ================    ===============================
        ``'-'``             solid line style
        ``'--'``            dashed line style
        ``'-.'``            dash-dot line style
        ``':'``             dotted line style
        ``'.'``             point marker
        ``','``             pixel marker
        ``'o'``             circle marker
        ``'v'``             triangle_down marker
        ``'^'``             triangle_up marker
        ``'<'``             triangle_left marker
        ``'>'``             triangle_right marker
        ``'1'``             tri_down marker
        ``'2'``             tri_up marker
        ``'3'``             tri_left marker
        ``'4'``             tri_right marker
        ``'s'``             square marker
        ``'p'``             pentagon marker
        ``'*'``             star marker
        ``'h'``             hexagon1 marker
        ``'H'``             hexagon2 marker
        ``'+'``             plus marker
        ``'x'``             x marker
        ``'D'``             diamond marker
        ``'d'``             thin_diamond marker
        ``'|'``             vline marker
        ``'_'``             hline marker
        ================    ===============================


        The following color abbreviations are supported:

        ==========  ========
        character   color
        ==========  ========
        'b'         blue
        'g'         green
        'r'         red
        'c'         cyan
        'm'         magenta
        'y'         yellow
        'k'         black
        'w'         white
        ==========  ========

        In addition, you can specify colors in many weird and
        wonderful ways, including full names (``'green'``), hex
        strings (``'#008000'``), RGB or RGBA tuples (``(0,1,0,1)``) or
        grayscale intensities as a string (``'0.8'``).  Of these, the
        string specifications can be used in place of a ``fmt`` group,
        but the tuple forms can be used only as ``kwargs``.

        Line styles and colors are combined in a single format string, as in
        ``'bo'`` for blue circles.

        The *kwargs* can be used to set line properties (any property that has
        a ``set_*`` method).  You can use this to set a line label (for auto
        legends), linewidth, anitialising, marker face color, etc.  Here is an
        example::

            plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)
            plot([1,2,3], [1,4,9], 'rs',  label='line 2')
            axis([0, 4, 0, 10])
            legend()

        If you make multiple lines with one plot command, the kwargs
        apply to all those lines, e.g.::

            plot(x1, y1, x2, y2, antialiased=False)

        Neither line will be antialiased.

        You do not need to use format strings, which are just
        abbreviations.  All of the line properties can be controlled
        by keyword arguments.  For example, you can set the color,
        marker, linestyle, and markercolor with::

            plot(x, y, color='green', linestyle='dashed', marker='o',
                 markerfacecolor='blue', markersize=12).

        See :class:`~matplotlib.lines.Line2D` for details.

        The kwargs are :class:`~matplotlib.lines.Line2D` properties:

        %(Line2D)s

        kwargs *scalex* and *scaley*, if defined, are passed on to
        :meth:`~matplotlib.axes.Axes.autoscale_view` to determine
        whether the *x* and *y* axes are autoscaled; the default is
        *True*.
        """
        scalex = kwargs.pop('scalex', True)
        scaley = kwargs.pop('scaley', True)

        if not self._hold:
            self.cla()
        lines = []

        kwargs = cbook.normalize_kwargs(kwargs, _alias_map)

        for line in self._get_lines(*args, **kwargs):
            self.add_line(line)
            lines.append(line)

        self.autoscale_view(scalex=scalex, scaley=scaley)
        return lines
