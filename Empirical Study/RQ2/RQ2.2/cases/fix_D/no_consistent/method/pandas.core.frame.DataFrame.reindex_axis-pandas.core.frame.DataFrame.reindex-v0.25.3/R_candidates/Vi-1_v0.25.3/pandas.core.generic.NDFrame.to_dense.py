    def to_dense(self):
        """
        Return dense representation of Series/DataFrame (as opposed to sparse).

        .. deprecated:: 0.25.0

        Returns
        -------
        %(klass)s
            Dense %(klass)s.
        """
        warnings.warn(
            "DataFrame/Series.to_dense is deprecated "
            "and will be removed in a future version",
            FutureWarning,
            stacklevel=2,
        )
        # compat
        return self
