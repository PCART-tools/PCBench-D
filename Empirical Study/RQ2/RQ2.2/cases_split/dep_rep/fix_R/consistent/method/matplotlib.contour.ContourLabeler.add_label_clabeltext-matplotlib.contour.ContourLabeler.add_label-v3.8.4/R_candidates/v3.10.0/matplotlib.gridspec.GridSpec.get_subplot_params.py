    def get_subplot_params(self, figure=None):
        """
        Return the `.SubplotParams` for the GridSpec.

        In order of precedence the values are taken from

        - non-*None* attributes of the GridSpec
        - the provided *figure*
        - :rc:`figure.subplot.*`

        Note that the ``figure`` attribute of the GridSpec is always ignored.
        """
        if figure is None:
            kw = {k: mpl.rcParams["figure.subplot."+k]
                  for k in self._AllowedKeys}
            subplotpars = SubplotParams(**kw)
        else:
            subplotpars = copy.copy(figure.subplotpars)

        subplotpars.update(**{k: getattr(self, k) for k in self._AllowedKeys})

        return subplotpars
