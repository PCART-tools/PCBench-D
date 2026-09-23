    @property
    def labels(self):
        warnings.warn((".labels was deprecated in version 0.24.0. "
                       "Use .codes instead."),
                      FutureWarning, stacklevel=2)
        return self.codes
