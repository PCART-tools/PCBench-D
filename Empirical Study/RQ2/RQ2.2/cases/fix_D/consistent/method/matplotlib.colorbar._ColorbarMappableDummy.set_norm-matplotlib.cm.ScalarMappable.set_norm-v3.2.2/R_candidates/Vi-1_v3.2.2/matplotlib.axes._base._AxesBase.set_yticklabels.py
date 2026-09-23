    def set_yticklabels(self, labels, fontdict=None, minor=False, **kwargs):
        """
        Set the y-tick labels with list of strings labels.

        Parameters
        ----------
        labels : List[str]
            list of string labels

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
        ----------------
        **kwargs : `~.text.Text` properties.
        """
        if fontdict is not None:
            kwargs.update(fontdict)
        return self.yaxis.set_ticklabels(labels,
                                         minor=minor, **kwargs)
