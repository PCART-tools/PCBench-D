    def add_gridspec(self, nrows=1, ncols=1, **kwargs):
        """
        Low-level API for creating a `.GridSpec` that has this figure as a parent.

        This is a low-level API, allowing you to create a gridspec and
        subsequently add subplots based on the gridspec. Most users do
        not need that freedom and should use the higher-level methods
        `~.Figure.subplots` or `~.Figure.subplot_mosaic`.

        Parameters
        ----------
        nrows : int, default: 1
            Number of rows in grid.

        ncols : int, default: 1
            Number of columns in grid.

        Returns
        -------
        `.GridSpec`

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
        return gs
