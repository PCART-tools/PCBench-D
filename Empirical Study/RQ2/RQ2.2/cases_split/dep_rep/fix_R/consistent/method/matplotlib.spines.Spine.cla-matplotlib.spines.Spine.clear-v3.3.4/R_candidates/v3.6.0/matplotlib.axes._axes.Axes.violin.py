    def violin(self, vpstats, positions=None, vert=True, widths=0.5,
               showmeans=False, showextrema=True, showmedians=False):
        """
        Drawing function for violin plots.

        Draw a violin plot for each column of *vpstats*. Each filled area
        extends to represent the entire data range, with optional lines at the
        mean, the median, the minimum, the maximum, and the quantiles values.

        Parameters
        ----------
        vpstats : list of dicts
          A list of dictionaries containing stats for each violin plot.
          Required keys are:

          - ``coords``: A list of scalars containing the coordinates that
            the violin's kernel density estimate were evaluated at.

          - ``vals``: A list of scalars containing the values of the
            kernel density estimate at each of the coordinates given
            in *coords*.

          - ``mean``: The mean value for this violin's dataset.

          - ``median``: The median value for this violin's dataset.

          - ``min``: The minimum value for this violin's dataset.

          - ``max``: The maximum value for this violin's dataset.

          Optional keys are:

          - ``quantiles``: A list of scalars containing the quantile values
            for this violin's dataset.

        positions : array-like, default: [1, 2, ..., n]
          The positions of the violins. The ticks and limits are
          automatically set to match the positions.

        vert : bool, default: True.
          If true, plots the violins vertically.
          Otherwise, plots the violins horizontally.

        widths : array-like, default: 0.5
          Either a scalar or a vector that sets the maximal width of
          each violin. The default is 0.5, which uses about half of the
          available horizontal space.

        showmeans : bool, default: False
          If true, will toggle rendering of the means.

        showextrema : bool, default: True
          If true, will toggle rendering of the extrema.

        showmedians : bool, default: False
          If true, will toggle rendering of the medians.

        Returns
        -------
        dict
          A dictionary mapping each component of the violinplot to a
          list of the corresponding collection instances created. The
          dictionary has the following keys:

          - ``bodies``: A list of the `~.collections.PolyCollection`
            instances containing the filled area of each violin.

          - ``cmeans``: A `~.collections.LineCollection` instance that marks
            the mean values of each of the violin's distribution.

          - ``cmins``: A `~.collections.LineCollection` instance that marks
            the bottom of each violin's distribution.

          - ``cmaxes``: A `~.collections.LineCollection` instance that marks
            the top of each violin's distribution.

          - ``cbars``: A `~.collections.LineCollection` instance that marks
            the centers of each violin's distribution.

          - ``cmedians``: A `~.collections.LineCollection` instance that
            marks the median values of each of the violin's distribution.

          - ``cquantiles``: A `~.collections.LineCollection` instance created
            to identify the quantiles values of each of the violin's
            distribution.
        """

        # Statistical quantities to be plotted on the violins
        means = []
        mins = []
        maxes = []
        medians = []
        quantiles = []

        qlens = []  # Number of quantiles in each dataset.

        artists = {}  # Collections to be returned

        N = len(vpstats)
        datashape_message = ("List of violinplot statistics and `{0}` "
                             "values must have the same length")

        # Validate positions
        if positions is None:
            positions = range(1, N + 1)
        elif len(positions) != N:
            raise ValueError(datashape_message.format("positions"))

        # Validate widths
        if np.isscalar(widths):
            widths = [widths] * N
        elif len(widths) != N:
            raise ValueError(datashape_message.format("widths"))

        # Calculate ranges for statistics lines (shape (2, N)).
        line_ends = [[-0.25], [0.25]] * np.array(widths) + positions

        # Colors.
        if mpl.rcParams['_internal.classic_mode']:
            fillcolor = 'y'
            linecolor = 'r'
        else:
            fillcolor = linecolor = self._get_lines.get_next_color()

        # Check whether we are rendering vertically or horizontally
        if vert:
            fill = self.fill_betweenx
            perp_lines = functools.partial(self.hlines, colors=linecolor)
            par_lines = functools.partial(self.vlines, colors=linecolor)
        else:
            fill = self.fill_between
            perp_lines = functools.partial(self.vlines, colors=linecolor)
            par_lines = functools.partial(self.hlines, colors=linecolor)

        # Render violins
        bodies = []
        for stats, pos, width in zip(vpstats, positions, widths):
            # The 0.5 factor reflects the fact that we plot from v-p to v+p.
            vals = np.array(stats['vals'])
            vals = 0.5 * width * vals / vals.max()
            bodies += [fill(stats['coords'], -vals + pos, vals + pos,
                            facecolor=fillcolor, alpha=0.3)]
            means.append(stats['mean'])
            mins.append(stats['min'])
            maxes.append(stats['max'])
            medians.append(stats['median'])
            q = stats.get('quantiles')  # a list of floats, or None
            if q is None:
                q = []
            quantiles.extend(q)
            qlens.append(len(q))
        artists['bodies'] = bodies

        if showmeans:  # Render means
            artists['cmeans'] = perp_lines(means, *line_ends)
        if showextrema:  # Render extrema
            artists['cmaxes'] = perp_lines(maxes, *line_ends)
            artists['cmins'] = perp_lines(mins, *line_ends)
            artists['cbars'] = par_lines(positions, mins, maxes)
        if showmedians:  # Render medians
            artists['cmedians'] = perp_lines(medians, *line_ends)
        if quantiles:  # Render quantiles: each width is repeated qlen times.
            artists['cquantiles'] = perp_lines(
                quantiles, *np.repeat(line_ends, qlens, axis=1))

        return artists
