    def reindex_axis(self, labels, axis=0, **kwargs):
        """ for compatibility with higher dims """
        if axis != 0:
            raise ValueError("cannot reindex series on non-zero axis!")
        return self.reindex(index=labels, **kwargs)
