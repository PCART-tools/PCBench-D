    @_api.make_keyword_only("3.9", "widths")
    def bxp(self, bxpstats, positions=None, widths=None, vert=None,
            orientation='vertical', patch_artist=False, shownotches=False,
            showmeans=False, showcaps=True, showbox=True, showfliers=True,
            boxprops=None, whiskerprops=None, flierprops=None,
            medianprops=None, capprops=None, meanprops=None,
            meanline=False, manage_ticks=True, zorder=None,
            capwidths=None, label=None):
        """
        Draw a box and whisker plot from pre-computed statistics.

        The box extends from the first quartile *q1* to the third
        quartile *q3* of the data, with a line at the median (*med*).
        The whiskers extend from *whislow* to *whishi*.
        Flier points are markers past the end of the whiskers.
        See https://en.wikipedia.org/wiki/Box_plot for reference.

        .. code-block:: none

                   whislow    q1    med    q3    whishi
                               |-----:-----|
               o      |--------|     :     |--------|    o  o
                               |-----:-----|
             flier                                      fliers

        .. note::
            This is a low-level drawing function for when you already
            have the statistical parameters. If you want a boxplot based
            on a dataset, use `~.Axes.boxplot` instead.

        Parameters
        ----------
        bxpstats : list of dicts
            A list of dictionaries containing stats for each boxplot.
            Required keys are:

            - ``med``: Median (scalar).
            - ``q1``, ``q3``: First & third quartiles (scalars).
            - ``whislo``, ``whishi``: Lower & upper whisker positions (scalars).

            Optional keys are:

            - ``mean``: Mean (scalar).  Needed if ``showmeans=True``.
            - ``fliers``: Data beyond the whiskers (array-like).
              Needed if ``showfliers=True``.
            - ``cilo``, ``cihi``: Lower & upper confidence intervals
              about the median. Needed if ``shownotches=True``.
            - ``label``: Name of the dataset (str).  If available,
              this will be used a tick label for the boxplot

        positions : array-like, default: [1, 2, ..., n]
            The positions of the boxes. The ticks and limits
            are automatically set to match the positions.

        widths : float or array-like, default: None
            The widths of the boxes.  The default is
            ``clip(0.15*(distance between extreme positions), 0.15, 0.5)``.

        capwidths : float or array-like, default: None
            Either a scalar or a vector and sets the width of each cap.
            The default is ``0.5*(width of the box)``, see *widths*.

        vert : bool, optional
            .. deprecated:: 3.11
                Use *orientation* instead.

                This is a pending deprecation for 3.10, with full deprecation
                in 3.11 and removal in 3.13.
                If this is given during the deprecation period, it overrides
                the *orientation* parameter.

            If True, plots the boxes vertically.
            If False, plots the boxes horizontally.

        orientation : {'vertical', 'horizontal'}, default: 'vertical'
            If 'horizontal', plots the boxes horizontally.
            Otherwise, plots the boxes vertically.

            .. versionadded:: 3.10

        patch_artist : bool, default: False
            If `False` produces boxes with the `.Line2D` artist.
            If `True` produces boxes with the `~matplotlib.patches.Patch` artist.

        shownotches, showmeans, showcaps, showbox, showfliers : bool
            Whether to draw the CI notches, the mean value (both default to
            False), the caps, the box, and the fliers (all three default to
            True).

        boxprops, whiskerprops, capprops, flierprops, medianprops, meanprops :\
 dict, optional
            Artist properties for the boxes, whiskers, caps, fliers, medians, and
            means.

        meanline : bool, default: False
            If `True` (and *showmeans* is `True`), will try to render the mean
            as a line spanning the full width of the box according to
            *meanprops*. Not recommended if *shownotches* is also True.
            Otherwise, means will be shown as points.

        manage_ticks : bool, default: True
            If True, the tick locations and labels will be adjusted to match the
            boxplot positions.

        label : str or list of str, optional
            Legend labels. Use a single string when all boxes have the same style and
            you only want a single legend entry for them. Use a list of strings to
            label all boxes individually. To be distinguishable, the boxes should be
            styled individually, which is currently only possible by modifying the
            returned artists, see e.g. :doc:`/gallery/statistics/boxplot_demo`.

            In the case of a single string, the legend entry will technically be
            associated with the first box only. By default, the legend will show the
            median line (``result["medians"]``); if *patch_artist* is True, the legend
            will show the box `.Patch` artists (``result["boxes"]``) instead.

            .. versionadded:: 3.9

        zorder : float, default: ``Line2D.zorder = 2``
            The zorder of the resulting boxplot.

        Returns
        -------
        dict
            A dictionary mapping each component of the boxplot to a list
            of the `.Line2D` instances created. That dictionary has the
            following keys (assuming vertical boxplots):

            - ``boxes``: main bodies of the boxplot showing the quartiles, and
              the median's confidence intervals if enabled.
            - ``medians``: horizontal lines at the median of each box.
            - ``whiskers``: vertical lines up to the last non-outlier data.
            - ``caps``: horizontal lines at the ends of the whiskers.
            - ``fliers``: points representing data beyond the whiskers (fliers).
            - ``means``: points or lines representing the means.

        See Also
        --------
        boxplot : Draw a boxplot from data instead of pre-computed statistics.
        """
        # Clamp median line to edge of box by default.
        medianprops = {
            "solid_capstyle": "butt",
            "dash_capstyle": "butt",
            **(medianprops or {}),
        }
        meanprops = {
            "solid_capstyle": "butt",
            "dash_capstyle": "butt",
            **(meanprops or {}),
        }

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

        def merge_kw_rc(subkey, explicit, zdelta=0, usemarker=True):
            d = {k.split('.')[-1]: v for k, v in mpl.rcParams.items()
                 if k.startswith(f'boxplot.{subkey}props')}
            d['zorder'] = zorder + zdelta
            if not usemarker:
                d['marker'] = ''
            d.update(cbook.normalize_kwargs(explicit, mlines.Line2D))
            return d

        box_kw = {
            'linestyle': mpl.rcParams['boxplot.boxprops.linestyle'],
            'linewidth': mpl.rcParams['boxplot.boxprops.linewidth'],
            'edgecolor': mpl.rcParams['boxplot.boxprops.color'],
            'facecolor': ('white' if mpl.rcParams['_internal.classic_mode']
                          else mpl.rcParams['patch.facecolor']),
            'zorder': zorder,
            **cbook.normalize_kwargs(boxprops, mpatches.PathPatch)
        } if patch_artist else merge_kw_rc('box', boxprops, usemarker=False)
        whisker_kw = merge_kw_rc('whisker', whiskerprops, usemarker=False)
        cap_kw = merge_kw_rc('cap', capprops, usemarker=False)
        flier_kw = merge_kw_rc('flier', flierprops)
        median_kw = merge_kw_rc('median', medianprops, zdelta, usemarker=False)
        mean_kw = merge_kw_rc('mean', meanprops, zdelta)
        removed_prop = 'marker' if meanline else 'linestyle'
        # Only remove the property if it's not set explicitly as a parameter.
        if meanprops is None or removed_prop not in meanprops:
            mean_kw[removed_prop] = ''

        # vert and orientation parameters are linked until vert's
        # deprecation period expires. vert only takes precedence
        # if set to False.
        if vert is None:
            vert = mpl.rcParams['boxplot.vertical']
        else:
            _api.warn_deprecated(
                "3.11",
                name="vert: bool",
                alternative="orientation: {'vertical', 'horizontal'}",
                pending=True,
            )
        if vert is False:
            orientation = 'horizontal'
        _api.check_in_list(['horizontal', 'vertical'], orientation=orientation)

        if not mpl.rcParams['boxplot.vertical']:
            _api.warn_deprecated(
                "3.10",
                name='boxplot.vertical', obj_type="rcparam"
            )

        # vertical or horizontal plot?
        maybe_swap = slice(None) if orientation == 'vertical' else slice(None, None, -1)

        def do_plot(xs, ys, **kwargs):
            return self.plot(*[xs, ys][maybe_swap], **kwargs)[0]

        def do_patch(xs, ys, **kwargs):
            path = mpath.Path._create_closed(
                np.column_stack([xs, ys][maybe_swap]))
            patch = mpatches.PathPatch(path, **kwargs)
            self.add_artist(patch)
            return patch

        # input validation
        N = len(bxpstats)
        datashape_message = ("List of boxplot statistics and `{0}` "
                             "values must have same the length")
        # check position
        if positions is None:
            positions = list(range(1, N + 1))
        elif len(positions) != N:
            raise ValueError(datashape_message.format("positions"))

        positions = np.array(positions)
        if len(positions) > 0 and not all(isinstance(p, Real) for p in positions):
            raise TypeError("positions should be an iterable of numbers")

        # width
        if widths is None:
            widths = [np.clip(0.15 * np.ptp(positions), 0.15, 0.5)] * N
        elif np.isscalar(widths):
            widths = [widths] * N
        elif len(widths) != N:
            raise ValueError(datashape_message.format("widths"))

        # capwidth
        if capwidths is None:
            capwidths = 0.5 * np.array(widths)
        elif np.isscalar(capwidths):
            capwidths = [capwidths] * N
        elif len(capwidths) != N:
            raise ValueError(datashape_message.format("capwidths"))

        for pos, width, stats, capwidth in zip(positions, widths, bxpstats,
                                               capwidths):
            # try to find a new label
            datalabels.append(stats.get('label', pos))

            # whisker coords
            whis_x = [pos, pos]
            whislo_y = [stats['q1'], stats['whislo']]
            whishi_y = [stats['q3'], stats['whishi']]
            # cap coords
            cap_left = pos - capwidth * 0.5
            cap_right = pos + capwidth * 0.5
            cap_x = [cap_left, cap_right]
            cap_lo = np.full(2, stats['whislo'])
            cap_hi = np.full(2, stats['whishi'])
            # box and median coords
            box_left = pos - width * 0.5
            box_right = pos + width * 0.5
            med_y = [stats['med'], stats['med']]
            # notched boxes
            if shownotches:
                notch_left = pos - width * 0.25
                notch_right = pos + width * 0.25
                box_x = [box_left, box_right, box_right, notch_right,
                         box_right, box_right, box_left, box_left, notch_left,
                         box_left, box_left]
                box_y = [stats['q1'], stats['q1'], stats['cilo'],
                         stats['med'], stats['cihi'], stats['q3'],
                         stats['q3'], stats['cihi'], stats['med'],
                         stats['cilo'], stats['q1']]
                med_x = [notch_left, notch_right]
            # plain boxes
            else:
                box_x = [box_left, box_right, box_right, box_left, box_left]
                box_y = [stats['q1'], stats['q1'], stats['q3'], stats['q3'],
                         stats['q1']]
                med_x = [box_left, box_right]

            # maybe draw the box
            if showbox:
                do_box = do_patch if patch_artist else do_plot
                boxes.append(do_box(box_x, box_y, **box_kw))
                median_kw.setdefault('label', '_nolegend_')
            # draw the whiskers
            whisker_kw.setdefault('label', '_nolegend_')
            whiskers.append(do_plot(whis_x, whislo_y, **whisker_kw))
            whiskers.append(do_plot(whis_x, whishi_y, **whisker_kw))
            # maybe draw the caps
            if showcaps:
                cap_kw.setdefault('label', '_nolegend_')
                caps.append(do_plot(cap_x, cap_lo, **cap_kw))
                caps.append(do_plot(cap_x, cap_hi, **cap_kw))
            # draw the medians
            medians.append(do_plot(med_x, med_y, **median_kw))
            # maybe draw the means
            if showmeans:
                if meanline:
                    means.append(do_plot(
                        [box_left, box_right], [stats['mean'], stats['mean']],
                        **mean_kw
                    ))
                else:
                    means.append(do_plot([pos], [stats['mean']], **mean_kw))
            # maybe draw the fliers
            if showfliers:
                flier_kw.setdefault('label', '_nolegend_')
                flier_x = np.full(len(stats['fliers']), pos, dtype=np.float64)
                flier_y = stats['fliers']
                fliers.append(do_plot(flier_x, flier_y, **flier_kw))

        # Set legend labels
        if label:
            box_or_med = boxes if showbox and patch_artist else medians
            if cbook.is_scalar_or_string(label):
                # assign the label only to the first box
                box_or_med[0].set_label(label)
            else:  # label is a sequence
                if len(box_or_med) != len(label):
                    raise ValueError(datashape_message.format("label"))
                for artist, lbl in zip(box_or_med, label):
                    artist.set_label(lbl)

        if manage_ticks:
            axis_name = "x" if orientation == 'vertical' else "y"
            interval = getattr(self.dataLim, f"interval{axis_name}")
            axis = self._axis_map[axis_name]
            positions = axis.convert_units(positions)
            # The 0.5 additional padding ensures reasonable-looking boxes
            # even when drawing a single box.  We set the sticky edge to
            # prevent margins expansion, in order to match old behavior (back
            # when separate calls to boxplot() would completely reset the axis
            # limits regardless of what was drawn before).  The sticky edges
            # are attached to the median lines, as they are always present.
            interval[:] = (min(interval[0], min(positions) - .5),
                           max(interval[1], max(positions) + .5))
            for median, position in zip(medians, positions):
                getattr(median.sticky_edges, axis_name).extend(
                    [position - .5, position + .5])
            # Modified from Axis.set_ticks and Axis.set_ticklabels.
            locator = axis.get_major_locator()
            if not isinstance(axis.get_major_locator(),
                              mticker.FixedLocator):
                locator = mticker.FixedLocator([])
                axis.set_major_locator(locator)
            locator.locs = np.array([*locator.locs, *positions])
            formatter = axis.get_major_formatter()
            if not isinstance(axis.get_major_formatter(),
                              mticker.FixedFormatter):
                formatter = mticker.FixedFormatter([])
                axis.set_major_formatter(formatter)
            formatter.seq = [*formatter.seq, *datalabels]

            self._request_autoscale_view()

        return dict(whiskers=whiskers, caps=caps, boxes=boxes,
                    medians=medians, fliers=fliers, means=means)
