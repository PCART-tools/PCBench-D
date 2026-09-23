    def subplots(self, nrows=1, ncols=1, sharex=False, sharey=False,
                 squeeze=True, subplot_kw=None, gridspec_kw=None):
        """
        Add a set of subplots to this figure.

        This utility wrapper makes it convenient to create common layouts of
        subplots in a single call.

        Parameters
        ----------
        nrows, ncols : int, optional, default: 1
            Number of rows/columns of the subplot grid.

        sharex, sharey : bool or {'none', 'all', 'row', 'col'}, default: False
            Controls sharing of properties among x (`sharex`) or y (`sharey`)
            axes:

            - True or 'all': x- or y-axis will be shared among all subplots.
            - False or 'none': each subplot x- or y-axis will be independent.
            - 'row': each subplot row will share an x- or y-axis.
            - 'col': each subplot column will share an x- or y-axis.

            When subplots have a shared x-axis along a column, only the x tick
            labels of the bottom subplot are created. Similarly, when subplots
            have a shared y-axis along a row, only the y tick labels of the
            first column subplot are created. To later turn other subplots'
            ticklabels on, use `~matplotlib.axes.Axes.tick_params`.

        squeeze : bool, optional, default: True
            - If True, extra dimensions are squeezed out from the returned
              array of Axes:

              - if only one subplot is constructed (nrows=ncols=1), the
                resulting single Axes object is returned as a scalar.
              - for Nx1 or 1xM subplots, the returned object is a 1D numpy
                object array of Axes objects.
              - for NxM, subplots with N>1 and M>1 are returned as a 2D array.

            - If False, no squeezing at all is done: the returned Axes object
              is always a 2D array containing Axes instances, even if it ends
              up being 1x1.

        subplot_kw : dict, optional
            Dict with keywords passed to the
            :meth:`~matplotlib.figure.Figure.add_subplot` call used to create
            each subplot.

        gridspec_kw : dict, optional
            Dict with keywords passed to the
            `~matplotlib.gridspec.GridSpec` constructor used to create
            the grid the subplots are placed on.

        Returns
        -------
        ax : `~.axes.Axes` object or array of Axes objects.
            *ax* can be either a single `~matplotlib.axes.Axes` object or
            an array of Axes objects if more than one subplot was created. The
            dimensions of the resulting array can be controlled with the
            squeeze keyword, see above.

        Examples
        --------
        ::

            # First create some toy data:
            x = np.linspace(0, 2*np.pi, 400)
            y = np.sin(x**2)

            # Create a figure
            plt.figure()

            # Create a subplot
            ax = fig.subplots()
            ax.plot(x, y)
            ax.set_title('Simple plot')

            # Create two subplots and unpack the output array immediately
            ax1, ax2 = fig.subplots(1, 2, sharey=True)
            ax1.plot(x, y)
            ax1.set_title('Sharing Y axis')
            ax2.scatter(x, y)

            # Create four polar axes and access them through the returned array
            axes = fig.subplots(2, 2, subplot_kw=dict(polar=True))
            axes[0, 0].plot(x, y)
            axes[1, 1].scatter(x, y)

            # Share a X axis with each column of subplots
            fig.subplots(2, 2, sharex='col')

            # Share a Y axis with each row of subplots
            fig.subplots(2, 2, sharey='row')

            # Share both X and Y axes with all subplots
            fig.subplots(2, 2, sharex='all', sharey='all')

            # Note that this is the same as
            fig.subplots(2, 2, sharex=True, sharey=True)

        See Also
        --------
        .pyplot.subplots
        .Figure.add_subplot
        .pyplot.subplot
        """

        if isinstance(sharex, bool):
            sharex = "all" if sharex else "none"
        if isinstance(sharey, bool):
            sharey = "all" if sharey else "none"
        # This check was added because it is very easy to type
        # `subplots(1, 2, 1)` when `subplot(1, 2, 1)` was intended.
        # In most cases, no error will ever occur, but mysterious behavior
        # will result because what was intended to be the subplot index is
        # instead treated as a bool for sharex.
        if isinstance(sharex, Integral):
            cbook._warn_external(
                "sharex argument to subplots() was an integer.  Did you "
                "intend to use subplot() (without 's')?")
        cbook._check_in_list(["all", "row", "col", "none"],
                             sharex=sharex, sharey=sharey)
        if subplot_kw is None:
            subplot_kw = {}
        if gridspec_kw is None:
            gridspec_kw = {}
        # don't mutate kwargs passed by user...
        subplot_kw = subplot_kw.copy()
        gridspec_kw = gridspec_kw.copy()

        if self.get_constrained_layout():
            gs = GridSpec(nrows, ncols, figure=self, **gridspec_kw)
        else:
            # this should turn constrained_layout off if we don't want it
            gs = GridSpec(nrows, ncols, figure=None, **gridspec_kw)
        self._gridspecs.append(gs)

        # Create array to hold all axes.
        axarr = np.empty((nrows, ncols), dtype=object)
        for row in range(nrows):
            for col in range(ncols):
                shared_with = {"none": None, "all": axarr[0, 0],
                               "row": axarr[row, 0], "col": axarr[0, col]}
                subplot_kw["sharex"] = shared_with[sharex]
                subplot_kw["sharey"] = shared_with[sharey]
                axarr[row, col] = self.add_subplot(gs[row, col], **subplot_kw)

        # turn off redundant tick labeling
        if sharex in ["col", "all"]:
            # turn off all but the bottom row
            for ax in axarr[:-1, :].flat:
                ax.xaxis.set_tick_params(which='both',
                                         labelbottom=False, labeltop=False)
                ax.xaxis.offsetText.set_visible(False)
        if sharey in ["row", "all"]:
            # turn off all but the first column
            for ax in axarr[:, 1:].flat:
                ax.yaxis.set_tick_params(which='both',
                                         labelleft=False, labelright=False)
                ax.yaxis.offsetText.set_visible(False)

        if squeeze:
            # Discarding unneeded dimensions that equal 1.  If we only have one
            # subplot, just return it instead of a 1-element array.
            return axarr.item() if axarr.size == 1 else axarr.squeeze()
        else:
            # Returned axis array will be always 2-d, even if nrows=ncols=1.
            return axarr
