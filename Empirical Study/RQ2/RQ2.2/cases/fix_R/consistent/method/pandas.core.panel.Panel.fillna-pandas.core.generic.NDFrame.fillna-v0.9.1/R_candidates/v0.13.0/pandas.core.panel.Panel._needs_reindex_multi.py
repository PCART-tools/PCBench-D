    def _needs_reindex_multi(self, axes, method, level):
        # only allowing multi-index on Panel (and not > dims)
        return (method is None and
                not self._is_mixed_type and
                self._AXIS_LEN <= 3 and
                com._count_not_none(*axes.values()) == 3)
