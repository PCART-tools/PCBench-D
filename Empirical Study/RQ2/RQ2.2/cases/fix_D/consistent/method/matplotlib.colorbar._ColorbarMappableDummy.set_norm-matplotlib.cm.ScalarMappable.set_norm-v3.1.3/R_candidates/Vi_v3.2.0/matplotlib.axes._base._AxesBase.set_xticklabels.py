    def set_xticklabels(self, labels, fontdict=None, minor=False, **kwargs):
        """
        Set the x-tick labels with list of string labels.

        Parameters
        ----------
        labels : List[str]
            List of string labels.

        fontdict : dict, optional
            A dictionary controlling the appearance of the ticklabels.
            The default *fontdict* is::

               {'fontsize': rcParams['axes.titlesize'],
                'fontweight': rcParams['axes.titleweight'],
                'verticalalignment': 'baseline',
                'horizontalalignment': loc}

        minor : bool, optional
            Whether to set the minor ticklabels rather than the major ones.

        Returns
        -------
        A list of `~.text.Text` instances.

        Other Parameters
        -----------------
        **kwargs : `~.text.Text` properties.
        """
        if fontdict is not None:
            kwargs.update(fontdict)
        ret = self.xaxis.set_ticklabels(labels,
                                        minor=minor, **kwargs)
        self.stale = True
        return ret
