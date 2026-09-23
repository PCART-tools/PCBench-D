    def bxp(self, bxpstats, positions=None, widths=None, vert=True,
            patch_artist=False, shownotches=False, showmeans=False,
            showcaps=True, showbox=True, showfliers=True,
            boxprops=None, whiskerprops=None, flierprops=None,
            medianprops=None, capprops=None, meanprops=None,
            meanline=False, manage_xticks=True, zorder=None):
        """
        Drawing function for box and whisker plots.

        Make a box and whisker plot for each column of *x* or each
        vector in sequence *x*.  The box extends from the lower to
        upper quartile values of the data, with a line at the median.
        The whiskers extend from the box to show the range of the
        data.  Flier points are those past the end of the whiskers.

        Parameters
        ----------

        bxpstats : list of dicts
          A list of dictionaries containing stats for each boxplot.
          Required keys are:

          - ``med``: The median (scalar float).

          - ``q1``: The first quartile (25th percentile) (scalar
            float).

          - ``q3``: The third quartile (75th percentile) (scalar
            float).

          - ``whislo``: Lower bound of the lower whisker (scalar
            float).

          - ``whishi``: Upper bound of the upper whisker (scalar
            float).

          Optional keys are:

          - ``mean``: The mean (scalar float). Needed if
            ``showmeans=True``.

          - ``fliers``: Data beyond the whiskers (sequence of floats).
            Needed if ``showfliers=True``.

          - ``cilo`` & ``cihi``: Lower and upper confidence intervals
            about the median. Needed if ``shownotches=True``.

          - ``label``: Name of the dataset (string). If available,
            this will be used a tick label for the boxplot

        positions : array-like, default = [1, 2, ..., n]
          Sets the positions of the boxes. The ticks and limits
          are automatically set to match the positions.

        widths : array-like, default = None
          Either a scalar or a vector and sets the width of each
          box. The default is ``0.15*(distance between extreme
          positions)``, clipped to no less than 0.15 and no more than
          0.5.

        vert : bool, default = False
          If `True` (default), makes the boxes vertical.  If `False`,
          makes horizontal boxes.

        patch_artist : bool, default = False
          If `False` produces boxes with the
          `~matplotlib.lines.Line2D` artist.  If `True` produces boxes
          with the `~matplotlib.patches.Patch` artist.

        shownotches : bool, default = False
          If `False` (default), produces a rectangular box plot.
          If `True`, will produce a notched box plot

        showmeans : bool, default = False
          If `True`, will toggle on the rendering of the means

        showcaps  : bool, default = True
          If `True`, will toggle on the rendering of the caps

        showbox  : bool, default = True
          If `True`, will toggle on the rendering of the box

        showfliers : bool, default = True
          If `True`, will toggle on the rendering of the fliers

        boxprops : dict or None (default)
          If provided, will set the plotting style of the boxes

        whiskerprops : dict or None (default)
          If provided, will set the plotting style of the whiskers

        capprops : dict or None (default)
          If provided, will set the plotting style of the caps

        flierprops : dict or None (default)
          If provided will set the plotting style of the fliers

        medianprops : dict or None (default)
          If provided, will set the plotting style of the medians

        meanprops : dict or None (default)
          If provided, will set the plotting style of the means

        meanline : bool, default = False
          If `True` (and *showmeans* is `True`), will try to render the mean
          as a line spanning the full width of the box according to
          *meanprops*. Not recommended if *shownotches* is also True.
          Otherwise, means will be shown as points.

        manage_xticks : bool, default = True
          If the function should adjust the xlim and xtick locations.

        zorder : scalar,  default = None
          The zorder of the resulting boxplot

        Returns
        -------
        result : dict
          A dictionary mapping each component of the boxplot to a list
          of the :class:`matplotlib.lines.Line2D` instances
          created. That dictionary has the following keys (assuming
          vertical boxplots):

          - ``boxes``: the main body of the boxplot showing the
            quartiles and the median's confidence intervals if
            enabled.

          - ``medians``: horizontal lines at the median of each box.

          - ``whiskers``: the vertical lines extending to the most
            extreme, non-outlier data points.

          - ``caps``: the horizontal lines at the ends of the
            whiskers.

          - ``fliers``: points representing data that extend beyond
            the whiskers (fliers).

          - ``means``: points or lines representing the means.

        Examples
        --------

        .. plot:: gallery/statistics/bxp.py

        """
        # lists of artists to be output
        whiskers = []
        caps = []
        boxes = []
        medians = []
        means = []
        fliers = []

        # empty list of xticklabels
        datalabels = []

        # Use default zorder if none specified
        if zorder is None:
            zorder = mlines.Line2D.zorder

        zdelta = 0.1
        # box properties
        if patch_artist:
            final_boxprops = dict(
                linestyle=rcParams['boxplot.boxprops.linestyle'],
                edgecolor=rcParams['boxplot.boxprops.color'],
                facecolor=rcParams['patch.facecolor'],
                linewidth=rcParams['boxplot.boxprops.linewidth']
            )
            if rcParams['_internal.classic_mode']:
                final_boxprops['facecolor'] = 'white'
        else:
            final_boxprops = dict(
                linestyle=rcParams['boxplot.boxprops.linestyle'],
                color=rcParams['boxplot.boxprops.color'],
            )

        final_boxprops['zorder'] = zorder
        if boxprops is not None:
            final_boxprops.update(boxprops)

        # other (cap, whisker) properties
        final_whiskerprops = dict(
            linestyle=rcParams['boxplot.whiskerprops.linestyle'],
            linewidth=rcParams['boxplot.whiskerprops.linewidth'],
            color=rcParams['boxplot.whiskerprops.color'],
        )

        final_capprops = dict(
            linestyle=rcParams['boxplot.capprops.linestyle'],
            linewidth=rcParams['boxplot.capprops.linewidth'],
            color=rcParams['boxplot.capprops.color'],
        )

        final_capprops['zorder'] = zorder
        if capprops is not None:
            final_capprops.update(capprops)

        final_whiskerprops['zorder'] = zorder
        if whiskerprops is not None:
            final_whiskerprops.update(whiskerprops)

        # set up the default flier properties
        final_flierprops = dict(
            linestyle=rcParams['boxplot.flierprops.linestyle'],
            linewidth=rcParams['boxplot.flierprops.linewidth'],
            color=rcParams['boxplot.flierprops.color'],
            marker=rcParams['boxplot.flierprops.marker'],
            markerfacecolor=rcParams['boxplot.flierprops.markerfacecolor'],
            markeredgecolor=rcParams['boxplot.flierprops.markeredgecolor'],
            markersize=rcParams['boxplot.flierprops.markersize'],
        )

        final_flierprops['zorder'] = zorder
        # flier (outlier) properties
        if flierprops is not None:
            final_flierprops.update(flierprops)

        # median line properties
        final_medianprops = dict(
            linestyle=rcParams['boxplot.medianprops.linestyle'],
            linewidth=rcParams['boxplot.medianprops.linewidth'],
            color=rcParams['boxplot.medianprops.color'],
        )
        final_medianprops['zorder'] = zorder + zdelta
        if medianprops is not None:
            final_medianprops.update(medianprops)

        # mean (line or point) properties
        if meanline:
            final_meanprops = dict(
                linestyle=rcParams['boxplot.meanprops.linestyle'],
                linewidth=rcParams['boxplot.meanprops.linewidth'],
                color=rcParams['boxplot.meanprops.color'],
            )
        else:
            final_meanprops = dict(
                linestyle='',
                marker=rcParams['boxplot.meanprops.marker'],
                markerfacecolor=rcParams['boxplot.meanprops.markerfacecolor'],
                markeredgecolor=rcParams['boxplot.meanprops.markeredgecolor'],
                markersize=rcParams['boxplot.meanprops.markersize'],
            )
        final_meanprops['zorder'] = zorder + zdelta
        if meanprops is not None:
            final_meanprops.update(meanprops)

        def to_vc(xs, ys):
            # convert arguments to verts and codes, append (0, 0) (ignored).
            verts = np.append(np.column_stack([xs, ys]), [(0, 0)], 0)
            codes = ([mpath.Path.MOVETO]
                     + [mpath.Path.LINETO] * (len(verts) - 2)
                     + [mpath.Path.CLOSEPOLY])
            return verts, codes

        def patch_list(xs, ys, **kwargs):
            verts, codes = to_vc(xs, ys)
            path = mpath.Path(verts, codes)
            patch = mpatches.PathPatch(path, **kwargs)
            self.add_artist(patch)
            return [patch]

        # vertical or horizontal plot?
        if vert:
            def doplot(*args, **kwargs):
                return self.plot(*args, **kwargs)

            def dopatch(xs, ys, **kwargs):
                return patch_list(xs, ys, **kwargs)

        else:
            def doplot(*args, **kwargs):
                shuffled = []
                for i in range(0, len(args), 2):
                    shuffled.extend([args[i + 1], args[i]])
                return self.plot(*shuffled, **kwargs)

            def dopatch(xs, ys, **kwargs):
                xs, ys = ys, xs  # flip X, Y
                return patch_list(xs, ys, **kwargs)

        # input validation
        N = len(bxpstats)
        datashape_message = ("List of boxplot statistics and `{0}` "
                             "values must have same the length")
        # check position
        if positions is None:
            positions = list(range(1, N + 1))
        elif len(positions) != N:
            raise ValueError(datashape_message.format("positions"))

        # width
        if widths is None:
            widths = [np.clip(0.15 * np.ptp(positions), 0.15, 0.5)] * N
        elif np.isscalar(widths):
            widths = [widths] * N
        elif len(widths) != N:
            raise ValueError(datashape_message.format("widths"))

        for pos, width, stats in zip(positions, widths, bxpstats):
            # try to find a new label
            datalabels.append(stats.get('label', pos))

            # whisker coords
            whisker_x = np.ones(2) * pos
            whiskerlo_y = np.array([stats['q1'], stats['whislo']])
            whiskerhi_y = np.array([stats['q3'], stats['whishi']])

            # cap coords
            cap_left = pos - width * 0.25
            cap_right = pos + width * 0.25
            cap_x = np.array([cap_left, cap_right])
            cap_lo = np.ones(2) * stats['whislo']
            cap_hi = np.ones(2) * stats['whishi']

            # box and median coords
            box_left = pos - width * 0.5
            box_right = pos + width * 0.5
            med_y = [stats['med'], stats['med']]

            # notched boxes
            if shownotches:
                box_x = [box_left, box_right, box_right, cap_right, box_right,
                         box_right, box_left, box_left, cap_left, box_left,
                         box_left]
                box_y = [stats['q1'], stats['q1'], stats['cilo'],
                         stats['med'], stats['cihi'], stats['q3'],
                         stats['q3'], stats['cihi'], stats['med'],
                         stats['cilo'], stats['q1']]
                med_x = cap_x

            # plain boxes
            else:
                box_x = [box_left, box_right, box_right, box_left, box_left]
                box_y = [stats['q1'], stats['q1'], stats['q3'], stats['q3'],
                         stats['q1']]
                med_x = [box_left, box_right]

            # maybe draw the box:
            if showbox:
                if patch_artist:
                    boxes.extend(dopatch(box_x, box_y, **final_boxprops))
                else:
                    boxes.extend(doplot(box_x, box_y, **final_boxprops))

            # draw the whiskers
            whiskers.extend(doplot(
                whisker_x, whiskerlo_y, **final_whiskerprops
            ))
            whiskers.extend(doplot(
                whisker_x, whiskerhi_y, **final_whiskerprops
            ))

            # maybe draw the caps:
            if showcaps:
                caps.extend(doplot(cap_x, cap_lo, **final_capprops))
                caps.extend(doplot(cap_x, cap_hi, **final_capprops))

            # draw the medians
            medians.extend(doplot(med_x, med_y, **final_medianprops))

            # maybe draw the means
            if showmeans:
                if meanline:
                    means.extend(doplot(
                        [box_left, box_right], [stats['mean'], stats['mean']],
                        **final_meanprops
                    ))
                else:
                    means.extend(doplot(
                        [pos], [stats['mean']], **final_meanprops
                    ))

            # maybe draw the fliers
            if showfliers:
                # fliers coords
                flier_x = np.ones(len(stats['fliers'])) * pos
                flier_y = stats['fliers']

                fliers.extend(doplot(
                    flier_x, flier_y, **final_flierprops
                ))

        # fix our axes/ticks up a little
        if vert:
            setticks = self.set_xticks
            setlim = self.set_xlim
            setlabels = self.set_xticklabels
        else:
            setticks = self.set_yticks
            setlim = self.set_ylim
            setlabels = self.set_yticklabels

        if manage_xticks:
            newlimits = min(positions) - 0.5, max(positions) + 0.5
            setlim(newlimits)
            setticks(positions)
            setlabels(datalabels)

        return dict(whiskers=whiskers, caps=caps, boxes=boxes,
                    medians=medians, fliers=fliers, means=means)
