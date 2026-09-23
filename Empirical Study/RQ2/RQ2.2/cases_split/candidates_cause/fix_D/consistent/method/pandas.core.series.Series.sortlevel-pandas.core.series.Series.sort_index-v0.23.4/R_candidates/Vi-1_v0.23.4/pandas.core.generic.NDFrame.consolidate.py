    def consolidate(self, inplace=False):
        """Compute NDFrame with "consolidated" internals (data of each dtype
        grouped together in a single ndarray).

        .. deprecated:: 0.20.0
            Consolidate will be an internal implementation only.
        """
        # 15483
        warnings.warn("consolidate is deprecated and will be removed in a "
                      "future release.", FutureWarning, stacklevel=2)
        return self._consolidate(inplace)
