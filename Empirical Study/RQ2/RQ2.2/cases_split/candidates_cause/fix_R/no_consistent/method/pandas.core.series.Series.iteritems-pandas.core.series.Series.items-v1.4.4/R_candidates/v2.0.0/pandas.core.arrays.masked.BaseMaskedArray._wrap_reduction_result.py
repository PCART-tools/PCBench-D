    def _wrap_reduction_result(self, name: str, result, skipna, **kwargs):
        if isinstance(result, np.ndarray):
            axis = kwargs["axis"]
            if skipna:
                # we only retain mask for all-NA rows/columns
                mask = self._mask.all(axis=axis)
            else:
                mask = self._mask.any(axis=axis)

            return self._maybe_mask_result(result, mask)
        return result
