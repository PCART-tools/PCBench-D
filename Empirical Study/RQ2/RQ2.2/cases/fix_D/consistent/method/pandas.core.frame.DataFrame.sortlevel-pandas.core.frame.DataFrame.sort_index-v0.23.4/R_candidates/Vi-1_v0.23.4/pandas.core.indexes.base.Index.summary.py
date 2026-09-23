    def summary(self, name=None):
        """
        Return a summarized representation
        .. deprecated:: 0.23.0
        """
        warnings.warn("'summary' is deprecated and will be removed in a "
                      "future version.", FutureWarning, stacklevel=2)
        return self._summary(name)
