    def _update_inplace(self, result, verify_is_copy=True):
        """
        replace self internals with result.

        Parameters
        ----------
        verify_is_copy : boolean, default True
            provide is_copy checks

        """
        # NOTE: This does *not* call __finalize__ and that's an explicit
        # decision that we may revisit in the future.

        self._reset_cache()
        self._clear_item_cache()
        self._data = getattr(result,'_data',result)
        self._maybe_update_cacher(verify_is_copy=verify_is_copy)
