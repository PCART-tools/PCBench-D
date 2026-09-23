    def _propagate_mask(
        self, mask: npt.NDArray[np.bool_] | None, other
    ) -> npt.NDArray[np.bool_]:
        if mask is None:
            mask = self._mask.copy()  # TODO: need test for BooleanArray needing a copy
            if other is libmissing.NA:
                # GH#45421 don't alter inplace
                mask = mask | True
        else:
            mask = self._mask | mask
        return mask
