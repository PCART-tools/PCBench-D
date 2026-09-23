    def get_subplot_params(self, figure=None):
        """
        Return a dictionary of subplot layout parameters. The default
        parameters are from rcParams unless a figure attribute is set.
        """
        if figure is None:
            kw = {k: rcParams["figure.subplot."+k] for k in self._AllowedKeys}
            subplotpars = mpl.figure.SubplotParams(**kw)
        else:
            subplotpars = copy.copy(figure.subplotpars)

        subplotpars.update(**{k: getattr(self, k) for k in self._AllowedKeys})

        return subplotpars
