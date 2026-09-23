    def to_sparse(self, *args, **kwargs):
        """
        NOT IMPLEMENTED: do not call this method, as sparsifying is not
        supported for Panel objects and will raise an error.

        Convert to SparsePanel
        """
        raise NotImplementedError("sparsifying is not supported "
                                  "for Panel objects")
