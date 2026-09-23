    def _needs_reindex_multi(self, axes, method, level: Level | None) -> bool_t:
        """Check if we do need a multi reindex."""
        return (
            (common.count_not_none(*axes.values()) == self._AXIS_LEN)
            and method is None
            and level is None
            # reindex_multi calls self.values, so we only want to go
            #  down that path when doing so is cheap.
            and self._can_fast_transpose
        )
