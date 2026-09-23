    def consolidate(self, inplace=False):
        """
        DEPRECATED: consolidate will be an internal implementation only.
        """
        # 15483
        warnings.warn("consolidate is deprecated and will be removed in a "
                      "future release.", FutureWarning, stacklevel=2)
        return self._consolidate(inplace)
