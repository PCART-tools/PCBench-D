    @docstring.dedent_interpd
    def set_thetagrids(self, angles, labels=None, frac=None, fmt=None,
                       **kwargs):
        """
        Set the angles at which to place the theta grids (these
        gridlines are equal along the theta dimension).  *angles* is in
        degrees.

        *labels*, if not None, is a ``len(angles)`` list of strings of
        the labels to use at each angle.

        If *labels* is None, the labels will be ``fmt %% angle``

        *frac* is the fraction of the polar axes radius at which to
        place the label (1 is the edge). e.g., 1.05 is outside the axes
        and 0.95 is inside the axes.

        Return value is a list of tuples (*line*, *label*), where
        *line* is :class:`~matplotlib.lines.Line2D` instances and the
        *label* is :class:`~matplotlib.text.Text` instances.

        kwargs are optional text properties for the labels:

        %(Text)s

        ACCEPTS: sequence of floats
        """
        # Make sure we take into account unitized data
        angles = self.convert_yunits(angles)
        angles = np.asarray(angles, float)
        self.set_xticks(angles * (np.pi / 180.0))
        if labels is not None:
            self.set_xticklabels(labels)
        elif fmt is not None:
            self.xaxis.set_major_formatter(mticker.FormatStrFormatter(fmt))
        for t in self.xaxis.get_ticklabels():
            t.update(kwargs)
        return self.xaxis.get_ticklines(), self.xaxis.get_ticklabels()
