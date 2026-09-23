    def iterkv(self, *args, **kwargs):
        "iteritems alias used to get around 2to3. Deprecated"
        warnings.warn("iterkv is deprecated and will be removed in a future "
                      "release, use ``iteritems`` instead.", FutureWarning,
                      stacklevel=2)
        return self.iteritems(*args, **kwargs)
