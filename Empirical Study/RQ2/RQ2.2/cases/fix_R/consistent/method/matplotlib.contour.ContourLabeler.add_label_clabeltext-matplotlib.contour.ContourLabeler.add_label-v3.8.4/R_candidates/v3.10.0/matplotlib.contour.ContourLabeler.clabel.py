    def clabel(self, levels=None, *,
               fontsize=None, inline=True, inline_spacing=5, fmt=None,
               colors=None, use_clabeltext=False, manual=False,
               rightside_up=True, zorder=None):
        """
        Label a contour plot.

        Adds labels to line contours in this `.ContourSet` (which inherits from
        this mixin class).

        Parameters
        ----------
        levels : array-like, optional
            A list of level values, that should be labeled. The list must be
            a subset of ``cs.levels``. If not given, all levels are labeled.

        fontsize : str or float, default: :rc:`font.size`
            Size in points or relative size e.g., 'smaller', 'x-large'.
            See `.Text.set_size` for accepted string values.

        colors : :mpltype:`color` or colors or None, default: None
            The label colors:

            - If *None*, the color of each label matches the color of
              the corresponding contour.

            - If one string color, e.g., *colors* = 'r' or *colors* =
              'red', all labels will be plotted in this color.

            - If a tuple of colors (string, float, RGB, etc), different labels
              will be plotted in different colors in the order specified.

        inline : bool, default: True
            If ``True`` the underlying contour is removed where the label is
            placed.

        inline_spacing : float, default: 5
            Space in pixels to leave on each side of label when placing inline.

            This spacing will be exact for labels at locations where the
            contour is straight, less so for labels on curved contours.

        fmt : `.Formatter` or str or callable or dict, optional
            How the levels are formatted:

            - If a `.Formatter`, it is used to format all levels at once, using
              its `.Formatter.format_ticks` method.
            - If a str, it is interpreted as a %-style format string.
            - If a callable, it is called with one level at a time and should
              return the corresponding label.
            - If a dict, it should directly map levels to labels.

            The default is to use a standard `.ScalarFormatter`.

        manual : bool or iterable, default: False
            If ``True``, contour labels will be placed manually using
            mouse clicks. Click the first button near a contour to
            add a label, click the second button (or potentially both
            mouse buttons at once) to finish adding labels. The third
            button can be used to remove the last label added, but
            only if labels are not inline. Alternatively, the keyboard
            can be used to select label locations (enter to end label
            placement, delete or backspace act like the third mouse button,
            and any other key will select a label location).

            *manual* can also be an iterable object of (x, y) tuples.
            Contour labels will be created as if mouse is clicked at each
            (x, y) position.

        rightside_up : bool, default: True
            If ``True``, label rotations will always be plus
            or minus 90 degrees from level.

        use_clabeltext : bool, default: False
            If ``True``, use `.Text.set_transform_rotates_text` to ensure that
            label rotation is updated whenever the Axes aspect changes.

        zorder : float or None, default: ``(2 + contour.get_zorder())``
            zorder of the contour labels.

        Returns
        -------
        labels
            A list of `.Text` instances for the labels.
        """

        # Based on the input arguments, clabel() adds a list of "label
        # specific" attributes to the ContourSet object.  These attributes are
        # all of the form label* and names should be fairly self explanatory.
        #
        # Once these attributes are set, clabel passes control to the labels()
        # method (for automatic label placement) or blocking_input_loop and
        # _contour_labeler_event_handler (for manual label placement).

        if fmt is None:
            fmt = ticker.ScalarFormatter(useOffset=False)
            fmt.create_dummy_axis()
        self.labelFmt = fmt
        self._use_clabeltext = use_clabeltext
        self.labelManual = manual
        self.rightside_up = rightside_up
        self._clabel_zorder = 2 + self.get_zorder() if zorder is None else zorder

        if levels is None:
            levels = self.levels
            indices = list(range(len(self.cvalues)))
        else:
            levlabs = list(levels)
            indices, levels = [], []
            for i, lev in enumerate(self.levels):
                if lev in levlabs:
                    indices.append(i)
                    levels.append(lev)
            if len(levels) < len(levlabs):
                raise ValueError(f"Specified levels {levlabs} don't match "
                                 f"available levels {self.levels}")
        self.labelLevelList = levels
        self.labelIndiceList = indices

        self._label_font_props = font_manager.FontProperties(size=fontsize)

        if colors is None:
            self.labelMappable = self
            self.labelCValueList = np.take(self.cvalues, self.labelIndiceList)
        else:
            cmap = mcolors.ListedColormap(colors, N=len(self.labelLevelList))
            self.labelCValueList = list(range(len(self.labelLevelList)))
            self.labelMappable = cm.ScalarMappable(cmap=cmap,
                                                   norm=mcolors.NoNorm())

        self.labelXYs = []

        if np.iterable(manual):
            for x, y in manual:
                self.add_label_near(x, y, inline, inline_spacing)
        elif manual:
            print('Select label locations manually using first mouse button.')
            print('End manual selection with second mouse button.')
            if not inline:
                print('Remove last label by clicking third mouse button.')
            mpl._blocking_input.blocking_input_loop(
                self.axes.get_figure(root=True),
                ["button_press_event", "key_press_event"],
                timeout=-1, handler=functools.partial(
                    _contour_labeler_event_handler,
                    self, inline, inline_spacing))
        else:
            self.labels(inline, inline_spacing)

        return cbook.silent_list('text.Text', self.labelTexts)
