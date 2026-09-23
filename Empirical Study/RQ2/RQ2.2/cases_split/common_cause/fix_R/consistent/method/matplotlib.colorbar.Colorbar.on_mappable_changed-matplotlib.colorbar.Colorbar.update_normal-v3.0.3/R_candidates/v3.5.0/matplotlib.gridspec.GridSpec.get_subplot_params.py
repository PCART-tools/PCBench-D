    def get_subplot_params(self, figure=None):
        """
        Return the `.SubplotParams` for the GridSpec.

        In order of precedence the values are taken from

        - non-*None* attributes of the GridSpec
        - the provided *figure*
        - :rc:`figure.subplot.*`
        """
        if figure is None:
            kw = {k: rcParams["figure.subplot."+k] for k in self._AllowedKeys}
            subplotpars = mpl.figure.SubplotParams(**kw)
        else:
            subplotpars = copy.copy(figure.subplotpars)

        subplotpars.update(**{k: getattr(self, k) for k in self._AllowedKeys})

        return subplotpars
