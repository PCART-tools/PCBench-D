    def clabel(self, *args,
               fontsize=None, inline=True, inline_spacing=5, fmt='%1.3f',
               colors=None, use_clabeltext=False, manual=False,
               rightside_up=True):
        """
        Label a contour plot.

        Call signature::

          clabel(cs, [levels,] **kwargs)

        Adds labels to line contours in *cs*, where *cs* is a
        :class:`~matplotlib.contour.ContourSet` object returned by
        ``contour()``.

        Parameters
        ----------
        cs : `.ContourSet`
            The ContourSet to label.

        levels : array-like, optional
            A list of level values, that should be labeled. The list must be
            a subset of ``cs.levels``. If not given, all levels are labeled.

        fontsize : string or float, optional
            Size in points or relative size e.g., 'smaller', 'x-large'.
            See `.Text.set_size` for accepted string values.

        colors : color-spec, optional
            The label colors:

            - If *None*, the color of each label matches the color of
              the corresponding contour.

            - If one string color, e.g., *colors* = 'r' or *colors* =
              'red', all labels will be plotted in this color.

            - If a tuple of matplotlib color args (string, float, rgb, etc),
              different labels will be plotted in different colors in the order
              specified.

        inline : bool, optional
            If ``True`` the underlying contour is removed where the label is
            placed. Default is ``True``.

        inline_spacing : float, optional
            Space in pixels to leave on each side of label when
            placing inline. Defaults to 5.

            This spacing will be exact for labels at locations where the
            contour is straight, less so for labels on curved contours.

        fmt : string or dict, optional
            A format string for the label. Default is '%1.3f'

            Alternatively, this can be a dictionary matching contour
            levels with arbitrary strings to use for each contour level
            (i.e., fmt[level]=string), or it can be any callable, such
            as a :class:`~matplotlib.ticker.Formatter` instance, that
            returns a string when called with a numeric contour level.

        manual : bool or iterable, optional
            If ``True``, contour labels will be placed manually using
            mouse clicks. Click the first button near a contour to
            add a label, click the second button (or potentially both
            mouse buttons at once) to finish adding labels. The third
            button can be used to remove the last label added, but
            only if labels are not inline. Alternatively, the keyboard
            can be used to select label locations (enter to end label
            placement, delete or backspace act like the third mouse button,
            and any other key will select a label location).

            *manual* can also be an iterable object of x,y tuples.
            Contour labels will be created as if mouse is clicked at each
            x,y positions.

        rightside_up : bool, optional
            If ``True``, label rotations will always be plus
            or minus 90 degrees from level. Default is ``True``.

        use_clabeltext : bool, optional
            If ``True``, `.ClabelText` class (instead of `.Text`) is used to
            create labels. `ClabelText` recalculates rotation angles
            of texts during the drawing time, therefore this can be used if
            aspect of the axes changes. Default is ``False``.

        Returns
        -------
        labels
            A list of `.Text` instances for the labels.
        """

        """
        NOTES on how this all works:

        clabel basically takes the input arguments and uses them to
        add a list of "label specific" attributes to the ContourSet
        object.  These attributes are all of the form label* and names
        should be fairly self explanatory.

        Once these attributes are set, clabel passes control to the
        labels method (case of automatic label placement) or
        `BlockingContourLabeler` (case of manual label placement).
        """

        self.labelFmt = fmt
        self._use_clabeltext = use_clabeltext
        # Detect if manual selection is desired and remove from argument list.
        self.labelManual = manual
        self.rightside_up = rightside_up

        if len(args) == 0:
            levels = self.levels
            indices = list(range(len(self.cvalues)))
        elif len(args) == 1:
            levlabs = list(args[0])
            indices, levels = [], []
            for i, lev in enumerate(self.levels):
                if lev in levlabs:
                    indices.append(i)
                    levels.append(lev)
            if len(levels) < len(levlabs):
                raise ValueError("Specified levels {} don't match available "
                                 "levels {}".format(levlabs, self.levels))
        else:
            raise TypeError("Illegal arguments to clabel, see help(clabel)")
        self.labelLevelList = levels
        self.labelIndiceList = indices

        self.labelFontProps = font_manager.FontProperties()
        self.labelFontProps.set_size(fontsize)
        font_size_pts = self.labelFontProps.get_size_in_points()
        self.labelFontSizeList = [font_size_pts] * len(levels)

        if colors is None:
            self.labelMappable = self
            self.labelCValueList = np.take(self.cvalues, self.labelIndiceList)
        else:
            cmap = mcolors.ListedColormap(colors, N=len(self.labelLevelList))
            self.labelCValueList = list(range(len(self.labelLevelList)))
            self.labelMappable = cm.ScalarMappable(cmap=cmap,
                                                   norm=mcolors.NoNorm())

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

        self.labelTextsList = cbook.silent_list('text.Text', self.labelTexts)
        return self.labelTextsList
