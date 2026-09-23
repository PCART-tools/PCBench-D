    def _get_labels(self):
        """
        Get the category labels (deprecated).

        Deprecated, use .codes!
        """
        import warnings
        warnings.warn("'labels' is deprecated. Use 'codes' instead", FutureWarning)
        return self.codes
