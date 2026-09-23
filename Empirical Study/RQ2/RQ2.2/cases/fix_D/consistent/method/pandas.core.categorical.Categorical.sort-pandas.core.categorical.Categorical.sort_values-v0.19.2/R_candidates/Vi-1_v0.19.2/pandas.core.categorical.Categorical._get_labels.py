    def _get_labels(self):
        """
        Get the category labels (deprecated).

        Deprecated, use .codes!
        """
        warn("'labels' is deprecated. Use 'codes' instead", FutureWarning,
             stacklevel=2)
        return self.codes
