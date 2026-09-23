    def clabel(self, *args, **kwargs):
        """
        Label a contour plot.

        Call signature::

          clabel(cs, **kwargs)

        Adds labels to line contours in *cs*, where *cs* is a
        :class:`~matplotlib.contour.ContourSet` object returned by
        contour.

        ::

          clabel(cs, v, **kwargs)

        only labels contours listed in *v*.

        Optional keyword arguments:

          *fontsize*:
            size in points or relative size e.g., 'smaller', 'x-large'

          *colors*:
            - if *None*, the color of each label matches the color of
              the corresponding contour

            - if one string color, e.g., *colors* = 'r' or *colors* =
              'red', all labels will be plotted in this color

            - if a tuple of matplotlib color args (string, float, rgb, etc),
              different labels will be plotted in different colors in the order
              specified

          *inline*:
            controls whether the underlying contour is removed or
            not. Default is *True*.

          *inline_spacing*:
            space in pixels to leave on each side of label when
            placing inline.  Defaults to 5.  This spacing will be
            exact for labels at locations where the contour is
            straight, less so for labels on curved contours.

          *fmt*:
            a format string for the label. Default is '%1.3f'
            Alternatively, this can be a dictionary matching contour
            levels with arbitrary strings to use for each contour level
            (i.e., fmt[level]=string), or it can be any callable, such
            as a :class:`~matplotlib.ticker.Formatter` instance, that
            returns a string when called with a numeric contour level.

          *manual*:
            if *True*, contour labels will be placed manually using
            mouse clicks.  Click the first button near a contour to
            add a label, click the second button (or potentially both
            mouse buttons at once) to finish adding labels.  The third
            button can be used to remove the last label added, but
            only if labels are not inline.  Alternatively, the keyboard
            can be used to select label locations (enter to end label
            placement, delete or backspace act like the third mouse button,
            and any other key will select a label location).

            *manual* can be an iterable object of x,y tuples. Contour labels
            will be created as if mouse is clicked at each x,y positions.

          *rightside_up*:
            if *True* (default), label rotations will always be plus
            or minus 90 degrees from level.

          *use_clabeltext*:
            if *True* (default is False), ClabelText class (instead of
            matplotlib.Text) is used to create labels. ClabelText
            recalculates rotation angles of texts during the drawing time,
            therefore this can be used if aspect of the axes changes.
        """

        """
        NOTES on how this all works:

        clabel basically takes the input arguments and uses them to
        add a list of "label specific" attributes to the ContourSet
        object.  These attributes are all of the form label* and names
        should be fairly self explanatory.

        Once these attributes are set, clabel passes control to the
        labels method (case of automatic label placement) or
        BlockingContourLabeler (case of manual label placement).
        """

        fontsize = kwargs.get('fontsize', None)
        inline = kwargs.get('inline', 1)
        inline_spacing = kwargs.get('inline_spacing', 5)
        self.labelFmt = kwargs.get('fmt', '%1.3f')
        _colors = kwargs.get('colors', None)

        self._use_clabeltext = kwargs.get('use_clabeltext', False)

        # Detect if manual selection is desired and remove from argument list
        self.labelManual = kwargs.get('manual', False)

        self.rightside_up = kwargs.get('rightside_up', True)
        if len(args) == 0:
            levels = self.levels
            indices = list(xrange(len(self.cvalues)))
        elif len(args) == 1:
            levlabs = list(args[0])
            indices, levels = [], []
            for i, lev in enumerate(self.levels):
                if lev in levlabs:
                    indices.append(i)
                    levels.append(lev)
            if len(levels) < len(levlabs):
                msg = "Specified levels " + str(levlabs)
                msg += "\n don't match available levels "
                msg += str(self.levels)
                raise ValueError(msg)
        else:
            raise TypeError("Illegal arguments to clabel, see help(clabel)")
        self.labelLevelList = levels
        self.labelIndiceList = indices

        self.labelFontProps = font_manager.FontProperties()
        self.labelFontProps.set_size(fontsize)
        font_size_pts = self.labelFontProps.get_size_in_points()
        self.labelFontSizeList = [font_size_pts] * len(levels)

        if _colors is None:
            self.labelMappable = self
            self.labelCValueList = np.take(self.cvalues, self.labelIndiceList)
        else:
            cmap = colors.ListedColormap(_colors, N=len(self.labelLevelList))
            self.labelCValueList = list(xrange(len(self.labelLevelList)))
            self.labelMappable = cm.ScalarMappable(cmap=cmap,
                                                   norm=colors.NoNorm())

        self.labelXYs = []

        if cbook.iterable(self.labelManual):
            for x, y in self.labelManual:
                self.add_label_near(x, y, inline,
                                    inline_spacing)

        elif self.labelManual:
            print('Select label locations manually using first mouse button.')
            print('End manual selection with second mouse button.')
            if not inline:
                print('Remove last label by clicking third mouse button.')

            blocking_contour_labeler = BlockingContourLabeler(self)
            blocking_contour_labeler(inline, inline_spacing)
        else:
            self.labels(inline, inline_spacing)

        # Hold on to some old attribute names.  These are deprecated and will
        # be removed in the near future (sometime after 2008-08-01), but
        # keeping for now for backwards compatibility
        self.cl = self.labelTexts
        self.cl_xy = self.labelXYs
        self.cl_cvalues = self.labelCValues

        self.labelTextsList = cbook.silent_list('text.Text', self.labelTexts)
        return self.labelTextsList
