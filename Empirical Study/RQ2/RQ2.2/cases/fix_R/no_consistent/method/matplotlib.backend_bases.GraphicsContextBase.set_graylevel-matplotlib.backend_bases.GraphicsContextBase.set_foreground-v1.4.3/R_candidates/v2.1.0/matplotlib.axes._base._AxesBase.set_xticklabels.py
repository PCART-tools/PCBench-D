    def set_xticklabels(self, labels, fontdict=None, minor=False, **kwargs):
        """
        Set the xtick labels with list of string labels

        Parameters
        ----------
        labels : list of str
            list of string labels

        fontdict : dict, optional
            A dictionary controlling the appearance of the ticklabels,
            the default `fontdict` is:

               {'fontsize': rcParams['axes.titlesize'],
                'fontweight' : rcParams['axes.titleweight'],
                'verticalalignment': 'baseline',
                'horizontalalignment': loc}

        minor : bool, optional
            If True select the minor ticklabels,
            else select the minor ticklabels

        Returns
        -------
        A list of `~matplotlib.text.Text` instances

        Other Parameters
        -----------------
        **kwargs : `~matplotlib.text.Text` properties.
        """
        if fontdict is not None:
            kwargs.update(fontdict)
        ret = self.xaxis.set_ticklabels(labels,
                                        minor=minor, **kwargs)
        self.stale = True
        return ret
