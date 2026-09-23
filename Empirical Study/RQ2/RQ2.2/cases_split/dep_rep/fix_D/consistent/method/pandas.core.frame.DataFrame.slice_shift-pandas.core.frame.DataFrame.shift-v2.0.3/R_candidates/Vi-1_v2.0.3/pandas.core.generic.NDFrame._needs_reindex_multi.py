    def _needs_reindex_multi(self, axes, method, level) -> bool_t:
        """Check if we do need a multi reindex."""
        return (
            (common.count_not_none(*axes.values()) == self._AXIS_LEN)
            and method is None
            and level is None
            and not self._is_mixed_type
            and not (
                self.ndim == 2
                and len(self.dtypes) == 1
                and is_extension_array_dtype(self.dtypes.iloc[0])
            )
        )
