    def add_gridspec(self, nrows, ncols, **kwargs):
        """
        Return a `.GridSpec` that has this figure as a parent.  This allows
        complex layout of axes in the figure.

        Parameters
        ----------
        nrows : int
            Number of rows in grid.

        ncols : int
            Number or columns in grid.

        Returns
        -------
        gridspec : `.GridSpec`

        Other Parameters
        ----------------
        **kwargs
            Keyword arguments are passed to `.GridSpec`.

        See Also
        --------
        matplotlib.pyplot.subplots

        Examples
        --------
        Adding a subplot that spans two rows::

            fig = plt.figure()
            gs = fig.add_gridspec(2, 2)
            ax1 = fig.add_subplot(gs[0, 0])
            ax2 = fig.add_subplot(gs[1, 0])
            # spans two rows:
            ax3 = fig.add_subplot(gs[:, 1])

        """

        _ = kwargs.pop('figure', None)  # pop in case user has added this...
        gs = GridSpec(nrows=nrows, ncols=ncols, figure=self, **kwargs)
        self._gridspecs.append(gs)
        return gs
