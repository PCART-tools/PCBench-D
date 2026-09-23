    def reindex_axis(self, labels, axis=0, **kwargs):
        """
        Conform Series to new index with optional filling logic.

        .. deprecated:: 0.21.0
            Use ``Series.reindex`` instead.
        """
        # for compatibility with higher dims
        if axis != 0:
            raise ValueError("cannot reindex series on non-zero axis!")
        msg = ("'.reindex_axis' is deprecated and will be removed in a future "
               "version. Use '.reindex' instead.")
        warnings.warn(msg, FutureWarning, stacklevel=2)

        return self.reindex(index=labels, **kwargs)
