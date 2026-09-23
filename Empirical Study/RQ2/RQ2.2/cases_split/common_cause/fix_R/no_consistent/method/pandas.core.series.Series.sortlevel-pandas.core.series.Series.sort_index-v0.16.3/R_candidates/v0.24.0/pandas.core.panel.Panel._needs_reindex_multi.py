    def _needs_reindex_multi(self, axes, method, level):
        """
        Don't allow a multi reindex on Panel or above ndim.
        """
        return False
