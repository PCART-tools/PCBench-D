    def __init__(self, ax, *args,
                 levels=None, filled=False, linewidths=None, linestyles=None,
                 alpha=None, origin=None, extent=None,
                 cmap=None, colors=None, norm=None, vmin=None, vmax=None,
                 extend='neither', antialiased=None,
                 **kwargs):
        """
        Draw contour lines or filled regions, depending on
        whether keyword arg *filled* is ``False`` (default) or ``True``.

        Call signature::

            ContourSet(ax, levels, allsegs, [allkinds], **kwargs)

        Parameters
        ----------
        ax : `~.axes.Axes`
            The `~.axes.Axes` object to draw on.

        levels : [level0, level1, ..., leveln]
            A list of floating point numbers indicating the contour
            levels.

        allsegs : [level0segs, level1segs, ...]
            List of all the polygon segments for all the *levels*.
            For contour lines ``len(allsegs) == len(levels)``, and for
            filled contour regions ``len(allsegs) = len(levels)-1``. The lists
            should look like::

                level0segs = [polygon0, polygon1, ...]
                polygon0 = array_like [[x0,y0], [x1,y1], ...]

        allkinds : [level0kinds, level1kinds, ...], optional
            Optional list of all the polygon vertex kinds (code types), as
            described and used in Path. This is used to allow multiply-
            connected paths such as holes within filled polygons.
            If not ``None``, ``len(allkinds) == len(allsegs)``. The lists
            should look like::

                level0kinds = [polygon0kinds, ...]
                polygon0kinds = [vertexcode0, vertexcode1, ...]

            If *allkinds* is not ``None``, usually all polygons for a
            particular contour level are grouped together so that
            ``level0segs = [polygon0]`` and ``level0kinds = [polygon0kinds]``.

        **kwargs
            Keyword arguments are as described in the docstring of
            `~axes.Axes.contour`.
        """
        self.ax = ax
        self.levels = levels
        self.filled = filled
        self.linewidths = linewidths
        self.linestyles = linestyles
        self.hatches = kwargs.pop('hatches', [None])
        self.alpha = alpha
        self.origin = origin
        self.extent = extent
        self.colors = colors
        self.extend = extend
        self.antialiased = antialiased
        if self.antialiased is None and self.filled:
            self.antialiased = False  # eliminate artifacts; we are not
                                      # stroking the boundaries.
            # The default for line contours will be taken from the
            # LineCollection default, which uses :rc:`lines.antialiased`.

        self.nchunk = kwargs.pop('nchunk', 0)
        self.locator = kwargs.pop('locator', None)
        if (isinstance(norm, mcolors.LogNorm)
                or isinstance(self.locator, ticker.LogLocator)):
            self.logscale = True
            if norm is None:
                norm = mcolors.LogNorm()
        else:
            self.logscale = False

        cbook._check_in_list([None, 'lower', 'upper', 'image'], origin=origin)
        if self.extent is not None and len(self.extent) != 4:
            raise ValueError("If given, *extent* must be '[ *None* |"
                             " (x0,x1,y0,y1) ]'")
        if self.colors is not None and cmap is not None:
            raise ValueError('Either colors or cmap must be None')
        if self.origin == 'image':
            self.origin = mpl.rcParams['image.origin']

        self._transform = kwargs.pop('transform', None)

        kwargs = self._process_args(*args, **kwargs)
        self._process_levels()

        if self.colors is not None:
            ncolors = len(self.levels)
            if self.filled:
                ncolors -= 1
            i0 = 0

            # Handle the case where colors are given for the extended
            # parts of the contour.
            extend_min = self.extend in ['min', 'both']
            extend_max = self.extend in ['max', 'both']
            use_set_under_over = False
            # if we are extending the lower end, and we've been given enough
            # colors then skip the first color in the resulting cmap. For the
            # extend_max case we don't need to worry about passing more colors
            # than ncolors as ListedColormap will clip.
            total_levels = ncolors + int(extend_min) + int(extend_max)
            if len(self.colors) == total_levels and (extend_min or extend_max):
                use_set_under_over = True
                if extend_min:
                    i0 = 1

            cmap = mcolors.ListedColormap(self.colors[i0:None], N=ncolors)

            if use_set_under_over:
                if extend_min:
                    cmap.set_under(self.colors[0])
                if extend_max:
                    cmap.set_over(self.colors[-1])

        if self.filled:
            self.collections = cbook.silent_list('mcoll.PathCollection')
        else:
            self.collections = cbook.silent_list('mcoll.LineCollection')
        # label lists must be initialized here
        self.labelTexts = []
        self.labelCValues = []

        kw = {'cmap': cmap}
        if norm is not None:
            kw['norm'] = norm
        # sets self.cmap, norm if needed;
        cm.ScalarMappable.__init__(self, **kw)
        if vmin is not None:
            self.norm.vmin = vmin
        if vmax is not None:
            self.norm.vmax = vmax
        self._process_colors()

        self.allsegs, self.allkinds = self._get_allsegs_and_allkinds()

        if self.filled:
            if self.linewidths is not None:
                cbook._warn_external('linewidths is ignored by contourf')

            # Lower and upper contour levels.
            lowers, uppers = self._get_lowers_and_uppers()

            # Ensure allkinds can be zipped below.
            if self.allkinds is None:
                self.allkinds = [None] * len(self.allsegs)

            # Default zorder taken from Collection
            zorder = kwargs.pop('zorder', 1)
            for level, level_upper, segs, kinds in \
                    zip(lowers, uppers, self.allsegs, self.allkinds):
                paths = self._make_paths(segs, kinds)

                col = mcoll.PathCollection(
                    paths,
                    antialiaseds=(self.antialiased,),
                    edgecolors='none',
                    alpha=self.alpha,
                    transform=self.get_transform(),
                    zorder=zorder)
                self.ax.add_collection(col, autolim=False)
                self.collections.append(col)
        else:
            tlinewidths = self._process_linewidths()
            self.tlinewidths = tlinewidths
            tlinestyles = self._process_linestyles()
            aa = self.antialiased
            if aa is not None:
                aa = (self.antialiased,)
            # Default zorder taken from LineCollection
            zorder = kwargs.pop('zorder', 2)
            for level, width, lstyle, segs in \
                    zip(self.levels, tlinewidths, tlinestyles, self.allsegs):
                col = mcoll.LineCollection(
                    segs,
                    antialiaseds=aa,
                    linewidths=width,
                    linestyles=[lstyle],
                    alpha=self.alpha,
                    transform=self.get_transform(),
                    zorder=zorder)
                col.set_label('_nolegend_')
                self.ax.add_collection(col, autolim=False)
                self.collections.append(col)

        for col in self.collections:
            col.sticky_edges.x[:] = [self._mins[0], self._maxs[0]]
            col.sticky_edges.y[:] = [self._mins[1], self._maxs[1]]
        self.ax.update_datalim([self._mins, self._maxs])
        self.ax.autoscale_view(tight=True)

        self.changed()  # set the colors

        if kwargs:
            s = ", ".join(map(repr, kwargs))
            cbook._warn_external('The following kwargs were not used by '
                                 'contour: ' + s)
