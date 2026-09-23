    def get_subplot_params(self, fig=None):
        """
        return a dictionary of subplot layout parameters. The default
        parameters are from rcParams unless a figure attribute is set.
        """
        from matplotlib.figure import SubplotParams
        if fig is None:
            kw = {k: rcParams["figure.subplot."+k] for k in self._AllowedKeys}
            subplotpars = SubplotParams(**kw)
        else:
            subplotpars = copy.copy(fig.subplotpars)

        update_kw = {k: getattr(self, k) for k in self._AllowedKeys}
        subplotpars.update(**update_kw)

        return subplotpars
