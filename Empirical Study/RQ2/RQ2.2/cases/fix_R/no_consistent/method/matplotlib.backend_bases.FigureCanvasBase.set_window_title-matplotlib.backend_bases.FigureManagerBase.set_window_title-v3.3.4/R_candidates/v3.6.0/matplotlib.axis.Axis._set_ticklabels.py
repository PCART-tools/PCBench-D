    def _set_ticklabels(self, labels, *, fontdict=None, minor=False, **kwargs):
        """
        Set this Axis' labels with list of string labels.

        .. warning::
            This method should only be used after fixing the tick positions
            using `.Axis.set_ticks`. Otherwise, the labels may end up in
            unexpected positions.

        Parameters
        ----------
        labels : list of str
            The label texts.

        fontdict : dict, optional
            A dictionary controlling the appearance of the ticklabels.
            The default *fontdict* is::

               {'fontsize': rcParams['axes.titlesize'],
                'fontweight': rcParams['axes.titleweight'],
                'verticalalignment': 'baseline',
                'horizontalalignment': loc}

        minor : bool, default: False
            Whether to set the minor ticklabels rather than the major ones.

        Returns
        -------
        list of `.Text`
            The labels.

        Other Parameters
        ----------------
        **kwargs : `~.text.Text` properties.
        """
        if fontdict is not None:
            kwargs.update(fontdict)
        return self.set_ticklabels(labels, minor=minor, **kwargs)
