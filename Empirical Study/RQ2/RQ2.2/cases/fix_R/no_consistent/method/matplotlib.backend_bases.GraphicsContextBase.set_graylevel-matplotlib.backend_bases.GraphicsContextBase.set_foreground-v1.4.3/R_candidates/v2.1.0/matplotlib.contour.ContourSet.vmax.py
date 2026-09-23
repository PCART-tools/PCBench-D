    @property
    def vmax(self):
        warnings.warn("vmax is deprecated and will be removed in 2.2 "
                      "and not replaced.",
                      mplDeprecation)
        return getattr(self, '_vmax', None)
