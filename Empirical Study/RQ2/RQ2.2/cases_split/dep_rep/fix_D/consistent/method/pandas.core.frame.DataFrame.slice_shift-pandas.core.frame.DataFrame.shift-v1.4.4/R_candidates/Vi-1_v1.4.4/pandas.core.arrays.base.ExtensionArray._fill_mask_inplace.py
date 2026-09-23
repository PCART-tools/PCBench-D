    def _fill_mask_inplace(
        self, method: str, limit, mask: npt.NDArray[np.bool_]
    ) -> None:
        """
        Replace values in locations specified by 'mask' using pad or backfill.

        See also
        --------
        ExtensionArray.fillna
        """
        func = missing.get_fill_func(method)
        # NB: if we don't copy mask here, it may be altered inplace, which
        #  would mess up the `self[mask] = ...` below.
        new_values, _ = func(self.astype(object), limit=limit, mask=mask.copy())
        new_values = self._from_sequence(new_values, dtype=self.dtype)
        self[mask] = new_values[mask]
        return
