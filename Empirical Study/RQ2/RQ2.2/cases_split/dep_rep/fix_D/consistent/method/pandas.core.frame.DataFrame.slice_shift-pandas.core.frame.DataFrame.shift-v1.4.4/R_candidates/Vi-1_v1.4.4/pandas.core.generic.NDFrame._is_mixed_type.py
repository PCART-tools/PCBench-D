    @final
    @property
    def _is_mixed_type(self) -> bool_t:
        if self._mgr.is_single_block:
            return False

        if self._mgr.any_extension_types:
            # Even if they have the same dtype, we can't consolidate them,
            #  so we pretend this is "mixed'"
            return True

        return self.dtypes.nunique() > 1
