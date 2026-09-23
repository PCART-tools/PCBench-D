    def set_labels(self, labels, level=None, inplace=False,
                   verify_integrity=True):
        warnings.warn((".set_labels was deprecated in version 0.24.0. "
                       "Use .set_codes instead."),
                      FutureWarning, stacklevel=2)
        return self.set_codes(codes=labels, level=level, inplace=inplace,
                              verify_integrity=verify_integrity)
