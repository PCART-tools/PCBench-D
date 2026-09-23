    @property
    def _values(self) -> np.ndarray | DatetimeArray | TimedeltaArray | PeriodArray:
        """
        Analogue to ._values that may return a 2D ExtensionArray.
        """
        mgr = self._mgr

        if isinstance(mgr, ArrayManager):
            if len(mgr.arrays) == 1 and not is_1d_only_ea_dtype(mgr.arrays[0].dtype):
                # error: Item "ExtensionArray" of "Union[ndarray, ExtensionArray]"
                # has no attribute "reshape"
                return mgr.arrays[0].reshape(-1, 1)  # type: ignore[union-attr]
            return ensure_wrapped_if_datetimelike(self.values)

        blocks = mgr.blocks
        if len(blocks) != 1:
            return ensure_wrapped_if_datetimelike(self.values)

        arr = blocks[0].values
        if arr.ndim == 1:
            # non-2D ExtensionArray
            return self.values

        # more generally, whatever we allow in NDArrayBackedExtensionBlock
        arr = cast("np.ndarray | DatetimeArray | TimedeltaArray | PeriodArray", arr)
        return arr.T
