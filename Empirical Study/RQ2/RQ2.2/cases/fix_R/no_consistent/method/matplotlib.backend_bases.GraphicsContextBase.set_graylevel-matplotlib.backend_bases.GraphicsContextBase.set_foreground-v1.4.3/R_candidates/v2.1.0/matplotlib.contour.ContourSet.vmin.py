    @property
    def vmin(self):
        warnings.warn("vmin is deprecated and will be removed in 2.2 "
                      "and not replaced.",
                      mplDeprecation)
        return getattr(self, '_vmin', None)
