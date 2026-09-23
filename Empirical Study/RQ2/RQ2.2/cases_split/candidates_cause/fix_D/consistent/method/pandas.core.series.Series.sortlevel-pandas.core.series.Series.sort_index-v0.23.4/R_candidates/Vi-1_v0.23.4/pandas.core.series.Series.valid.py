    def valid(self, inplace=False, **kwargs):
        """Return Series without null values.

        .. deprecated:: 0.23.0
            Use :meth:`Series.dropna` instead.
        """
        warnings.warn("Method .valid will be removed in a future version. "
                      "Use .dropna instead.", FutureWarning, stacklevel=2)
        return self.dropna(inplace=inplace, **kwargs)
