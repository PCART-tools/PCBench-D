    @final
    def _update_inplace(self, result, verify_is_copy: bool_t = True) -> None:
        """
        Replace self internals with result.

        Parameters
        ----------
        result : same type as self
        verify_is_copy : bool, default True
            Provide is_copy checks.
        """
        # NOTE: This does *not* call __finalize__ and that's an explicit
        # decision that we may revisit in the future.
        self._reset_cache()
        self._clear_item_cache()
        self._mgr = result._mgr
        self._maybe_update_cacher(verify_is_copy=verify_is_copy, inplace=True)
