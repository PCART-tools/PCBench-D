    def irow(self, i):
        """
        DEPRECATED. Use ``.nth(i)`` instead
        """

        # 10177
        warnings.warn("irow(i) is deprecated. Please use .nth(i)",
                      FutureWarning, stacklevel=2)
        return self.nth(i)
