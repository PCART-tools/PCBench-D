class ContourLabeler:
    """Mixin to provide labelling capability to `.ContourSet`."""

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

        colors : color or colors or None, default: None
            The label colors:

            - If *None*, the color of each label matches the color of
              the corresponding contour.

            - If one string color, e.g., *colors* = 'r' or *colors* =
              'red', all labels will be plotted in this color.

            - If a tuple of colors (string, float, rgb, etc), different labels
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
            If ``True``, `.ClabelText` class (instead of `.Text`) is used to
            create labels. `ClabelText` recalculates rotation angles
            of texts during the drawing time, therefore this can be used if
            aspect of the axes changes.

        zorder : float or None, default: ``(2 + contour.get_zorder())``
            zorder of the contour labels.

        Returns
        -------
        labels
            A list of `.Text` instances for the labels.
        """

        # clabel basically takes the input arguments and uses them to
        # add a list of "label specific" attributes to the ContourSet
        # object.  These attributes are all of the form label* and names
        # should be fairly self explanatory.
        #
        # Once these attributes are set, clabel passes control to the
        # labels method (case of automatic label placement) or
        # `BlockingContourLabeler` (case of manual label placement).

        if fmt is None:
            fmt = ticker.ScalarFormatter(useOffset=False)
            fmt.create_dummy_axis()
        self.labelFmt = fmt
        self._use_clabeltext = use_clabeltext
        # Detect if manual selection is desired and remove from argument list.
        self.labelManual = manual
        self.rightside_up = rightside_up
        if zorder is None:
            self._clabel_zorder = 2+self._contour_zorder
        else:
            self._clabel_zorder = zorder

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

        if np.iterable(self.labelManual):
            for x, y in self.labelManual:
                self.add_label_near(x, y, inline, inline_spacing)
        elif self.labelManual:
            print('Select label locations manually using first mouse button.')
            print('End manual selection with second mouse button.')
            if not inline:
                print('Remove last label by clicking third mouse button.')
            mpl._blocking_input.blocking_input_loop(
                self.axes.figure, ["button_press_event", "key_press_event"],
                timeout=-1, handler=functools.partial(
                    _contour_labeler_event_handler,
                    self, inline, inline_spacing))
        else:
            self.labels(inline, inline_spacing)

        self.labelTextsList = cbook.silent_list('text.Text', self.labelTexts)
        return self.labelTextsList

    def print_label(self, linecontour, labelwidth):
        """Return whether a contour is long enough to hold a label."""
        return (len(linecontour) > 10 * labelwidth
                or (np.ptp(linecontour, axis=0) > 1.2 * labelwidth).any())

    def too_close(self, x, y, lw):
        """Return whether a label is already near this location."""
        thresh = (1.2 * lw) ** 2
        return any((x - loc[0]) ** 2 + (y - loc[1]) ** 2 < thresh
                   for loc in self.labelXYs)

    @_api.deprecated("3.4")
    def get_label_coords(self, distances, XX, YY, ysize, lw):
        """
        Return x, y, and the index of a label location.

        Labels are plotted at a location with the smallest
        deviation of the contour from a straight line
        unless there is another label nearby, in which case
        the next best place on the contour is picked up.
        If all such candidates are rejected, the beginning
        of the contour is chosen.
        """
        hysize = int(ysize / 2)
        adist = np.argsort(distances)

        for ind in adist:
            x, y = XX[ind][hysize], YY[ind][hysize]
            if self.too_close(x, y, lw):
                continue
            return x, y, ind

        ind = adist[0]
        x, y = XX[ind][hysize], YY[ind][hysize]
        return x, y, ind

    def _get_nth_label_width(self, nth):
        """Return the width of the *nth* label, in pixels."""
        fig = self.axes.figure
        return (
            text.Text(0, 0,
                      self.get_text(self.labelLevelList[nth], self.labelFmt),
                      figure=fig,
                      size=self.labelFontSizeList[nth],
                      fontproperties=self.labelFontProps)
            .get_window_extent(mpl.tight_layout.get_renderer(fig)).width)

    @_api.deprecated("3.5")
    def get_label_width(self, lev, fmt, fsize):
        """Return the width of the label in points."""
        if not isinstance(lev, str):
            lev = self.get_text(lev, fmt)
        fig = self.axes.figure
        width = (text.Text(0, 0, lev, figure=fig,
                           size=fsize, fontproperties=self.labelFontProps)
                 .get_window_extent(mpl.tight_layout.get_renderer(fig)).width)
        width *= 72 / fig.dpi
        return width

    def set_label_props(self, label, text, color):
        """Set the label properties - color, fontsize, text."""
        label.set_text(text)
        label.set_color(color)
        label.set_fontproperties(self.labelFontProps)
        label.set_clip_box(self.axes.bbox)

    def get_text(self, lev, fmt):
        """Get the text of the label."""
        if isinstance(lev, str):
            return lev
        elif isinstance(fmt, dict):
            return fmt.get(lev, '%1.3f')
        elif callable(getattr(fmt, "format_ticks", None)):
            return fmt.format_ticks([*self.labelLevelList, lev])[-1]
        elif callable(fmt):
            return fmt(lev)
        else:
            return fmt % lev

    def locate_label(self, linecontour, labelwidth):
        """
        Find good place to draw a label (relatively flat part of the contour).
        """
        ctr_size = len(linecontour)
        n_blocks = int(np.ceil(ctr_size / labelwidth)) if labelwidth > 1 else 1
        block_size = ctr_size if n_blocks == 1 else int(labelwidth)
        # Split contour into blocks of length ``block_size``, filling the last
        # block by cycling the contour start (per `np.resize` semantics).  (Due
        # to cycling, the index returned is taken modulo ctr_size.)
        xx = np.resize(linecontour[:, 0], (n_blocks, block_size))
        yy = np.resize(linecontour[:, 1], (n_blocks, block_size))
        yfirst = yy[:, :1]
        ylast = yy[:, -1:]
        xfirst = xx[:, :1]
        xlast = xx[:, -1:]
        s = (yfirst - yy) * (xlast - xfirst) - (xfirst - xx) * (ylast - yfirst)
        l = np.hypot(xlast - xfirst, ylast - yfirst)
        # Ignore warning that divide by zero throws, as this is a valid option
        with np.errstate(divide='ignore', invalid='ignore'):
            distances = (abs(s) / l).sum(axis=-1)
        # Labels are drawn in the middle of the block (``hbsize``) where the
        # contour is the closest (per ``distances``) to a straight line, but
        # not `too_close()` to a preexisting label.
        hbsize = block_size // 2
        adist = np.argsort(distances)
        # If all candidates are `too_close()`, go back to the straightest part
        # (``adist[0]``).
        for idx in np.append(adist, adist[0]):
            x, y = xx[idx, hbsize], yy[idx, hbsize]
            if not self.too_close(x, y, labelwidth):
                break
        return x, y, (idx * block_size + hbsize) % ctr_size

    def calc_label_rot_and_inline(self, slc, ind, lw, lc=None, spacing=5):
        """
        Calculate the appropriate label rotation given the linecontour
        coordinates in screen units, the index of the label location and the
        label width.

        If *lc* is not None or empty, also break contours and compute
        inlining.

        *spacing* is the empty space to leave around the label, in pixels.

        Both tasks are done together to avoid calculating path lengths
        multiple times, which is relatively costly.

        The method used here involves computing the path length along the
        contour in pixel coordinates and then looking approximately (label
        width / 2) away from central point to determine rotation and then to
        break contour if desired.
        """

        if lc is None:
            lc = []
        # Half the label width
        hlw = lw / 2.0

        # Check if closed and, if so, rotate contour so label is at edge
        closed = _is_closed_polygon(slc)
        if closed:
            slc = np.concatenate([slc[ind:-1], slc[:ind + 1]])
            if len(lc):  # Rotate lc also if not empty
                lc = np.concatenate([lc[ind:-1], lc[:ind + 1]])
            ind = 0

        # Calculate path lengths
        pl = np.zeros(slc.shape[0], dtype=float)
        dx = np.diff(slc, axis=0)
        pl[1:] = np.cumsum(np.hypot(dx[:, 0], dx[:, 1]))
        pl = pl - pl[ind]

        # Use linear interpolation to get points around label
        xi = np.array([-hlw, hlw])
        if closed:  # Look at end also for closed contours
            dp = np.array([pl[-1], 0])
        else:
            dp = np.zeros_like(xi)

        # Get angle of vector between the two ends of the label - must be
        # calculated in pixel space for text rotation to work correctly.
        (dx,), (dy,) = (np.diff(np.interp(dp + xi, pl, slc_col))
                        for slc_col in slc.T)
        rotation = np.rad2deg(np.arctan2(dy, dx))

        if self.rightside_up:
            # Fix angle so text is never upside-down
            rotation = (rotation + 90) % 180 - 90

        # Break contour if desired
        nlc = []
        if len(lc):
            # Expand range by spacing
            xi = dp + xi + np.array([-spacing, spacing])

            # Get (integer) indices near points of interest; use -1 as marker
            # for out of bounds.
            I = np.interp(xi, pl, np.arange(len(pl)), left=-1, right=-1)
            I = [np.floor(I[0]).astype(int), np.ceil(I[1]).astype(int)]
            if I[0] != -1:
                xy1 = [np.interp(xi[0], pl, lc_col) for lc_col in lc.T]
            if I[1] != -1:
                xy2 = [np.interp(xi[1], pl, lc_col) for lc_col in lc.T]

            # Actually break contours
            if closed:
                # This will remove contour if shorter than label
                if all(i != -1 for i in I):
                    nlc.append(np.row_stack([xy2, lc[I[1]:I[0]+1], xy1]))
            else:
                # These will remove pieces of contour if they have length zero
                if I[0] != -1:
                    nlc.append(np.row_stack([lc[:I[0]+1], xy1]))
                if I[1] != -1:
                    nlc.append(np.row_stack([xy2, lc[I[1]:]]))

            # The current implementation removes contours completely
            # covered by labels.  Uncomment line below to keep
            # original contour if this is the preferred behavior.
            # if not len(nlc): nlc = [ lc ]

        return rotation, nlc

    def _get_label_text(self, x, y, rotation):
        dx, dy = self.axes.transData.inverted().transform((x, y))
        t = text.Text(dx, dy, rotation=rotation,
                      horizontalalignment='center',
                      verticalalignment='center', zorder=self._clabel_zorder)
        return t

    def _get_label_clabeltext(self, x, y, rotation):
        # x, y, rotation is given in pixel coordinate. Convert them to
        # the data coordinate and create a label using ClabelText
        # class. This way, the rotation of the clabel is along the
        # contour line always.
        transDataInv = self.axes.transData.inverted()
        dx, dy = transDataInv.transform((x, y))
        drotation = transDataInv.transform_angles(np.array([rotation]),
                                                  np.array([[x, y]]))
        t = ClabelText(dx, dy, rotation=drotation[0],
                       horizontalalignment='center',
                       verticalalignment='center', zorder=self._clabel_zorder)

        return t

    def _add_label(self, t, x, y, lev, cvalue):
        color = self.labelMappable.to_rgba(cvalue, alpha=self.alpha)

        _text = self.get_text(lev, self.labelFmt)
        self.set_label_props(t, _text, color)
        self.labelTexts.append(t)
        self.labelCValues.append(cvalue)
        self.labelXYs.append((x, y))

        # Add label to plot here - useful for manual mode label selection
        self.axes.add_artist(t)

    def add_label(self, x, y, rotation, lev, cvalue):
        """
        Add contour label using :class:`~matplotlib.text.Text` class.
        """
        t = self._get_label_text(x, y, rotation)
        self._add_label(t, x, y, lev, cvalue)

    def add_label_clabeltext(self, x, y, rotation, lev, cvalue):
        """
        Add contour label using :class:`ClabelText` class.
        """
        # x, y, rotation is given in pixel coordinate. Convert them to
        # the data coordinate and create a label using ClabelText
        # class. This way, the rotation of the clabel is along the
        # contour line always.
        t = self._get_label_clabeltext(x, y, rotation)
        self._add_label(t, x, y, lev, cvalue)

    def add_label_near(self, x, y, inline=True, inline_spacing=5,
                       transform=None):
        """
        Add a label near the point ``(x, y)``.

        Parameters
        ----------
        x, y : float
            The approximate location of the label.
        inline : bool, default: True
            If *True* remove the segment of the contour beneath the label.
        inline_spacing : int, default: 5
            Space in pixels to leave on each side of label when placing
            inline. This spacing will be exact for labels at locations where
            the contour is straight, less so for labels on curved contours.
        transform : `.Transform` or `False`, default: ``self.axes.transData``
            A transform applied to ``(x, y)`` before labeling.  The default
            causes ``(x, y)`` to be interpreted as data coordinates.  `False`
            is a synonym for `.IdentityTransform`; i.e. ``(x, y)`` should be
            interpreted as display coordinates.
        """

        if transform is None:
            transform = self.axes.transData
        if transform:
            x, y = transform.transform((x, y))

        # find the nearest contour _in screen units_
        conmin, segmin, imin, xmin, ymin = self.find_nearest_contour(
            x, y, self.labelIndiceList)[:5]

        # calc_label_rot_and_inline() requires that (xmin, ymin)
        # be a vertex in the path. So, if it isn't, add a vertex here
        paths = self.collections[conmin].get_paths()  # paths of correct coll.
        lc = paths[segmin].vertices  # vertices of correct segment
        # Where should the new vertex be added in data-units?
        xcmin = self.axes.transData.inverted().transform([xmin, ymin])
        if not np.allclose(xcmin, lc[imin]):
            # No vertex is close enough, so add a new point in the vertices and
            # replace the path by the new one.
            lc = np.insert(lc, imin, xcmin, axis=0)
            paths[segmin] = mpath.Path(lc)

        # Get index of nearest level in subset of levels used for labeling
        lmin = self.labelIndiceList.index(conmin)

        # Get label width for rotating labels and breaking contours
        lw = self._get_nth_label_width(lmin)

        # Figure out label rotation.
        rotation, nlc = self.calc_label_rot_and_inline(
            self.axes.transData.transform(lc),  # to pixel space.
            imin, lw, lc if inline else None, inline_spacing)

        self.add_label(xmin, ymin, rotation, self.labelLevelList[lmin],
                       self.labelCValueList[lmin])

        if inline:
            # Remove old, not looping over paths so we can do this up front
            paths.pop(segmin)

            # Add paths if not empty or single point
            for n in nlc:
                if len(n) > 1:
                    paths.append(mpath.Path(n))

    def pop_label(self, index=-1):
        """Defaults to removing last label, but any index can be supplied"""
        self.labelCValues.pop(index)
        t = self.labelTexts.pop(index)
        t.remove()

    def labels(self, inline, inline_spacing):

        if self._use_clabeltext:
            add_label = self.add_label_clabeltext
        else:
            add_label = self.add_label

        for idx, (icon, lev, cvalue) in enumerate(zip(
                self.labelIndiceList,
                self.labelLevelList,
                self.labelCValueList,
        )):

            con = self.collections[icon]
            trans = con.get_transform()
            lw = self._get_nth_label_width(idx)
            additions = []
            paths = con.get_paths()
            for segNum, linepath in enumerate(paths):
                lc = linepath.vertices  # Line contour
                slc = trans.transform(lc)  # Line contour in screen coords

                # Check if long enough for a label
                if self.print_label(slc, lw):
                    x, y, ind = self.locate_label(slc, lw)

                    rotation, new = self.calc_label_rot_and_inline(
                        slc, ind, lw, lc if inline else None, inline_spacing)

                    # Actually add the label
                    add_label(x, y, rotation, lev, cvalue)

                    # If inline, add new contours
                    if inline:
                        for n in new:
                            # Add path if not empty or single point
                            if len(n) > 1:
                                additions.append(mpath.Path(n))
                else:  # If not adding label, keep old path
                    additions.append(linepath)

            # After looping over all segments on a contour, replace old paths
            # by new ones if inlining.
            if inline:
                paths[:] = additions
