    def add_subfigure(self, subplotspec, **kwargs):
        """
        Add a `~.figure.SubFigure` to the figure as part of a subplot
        arrangement.

        Parameters
        ----------
        subplotspec : `.gridspec.SubplotSpec`
            Defines the region in a parent gridspec where the subfigure will
            be placed.

        Returns
        -------
        `.figure.SubFigure`

        Other Parameters
        ----------------
        **kwargs
            Are passed to the `~.figure.SubFigure` object.

        See Also
        --------
        .Figure.subfigures
        """
        sf = SubFigure(self, subplotspec, **kwargs)
        self.subfigs += [sf]
        return sf
