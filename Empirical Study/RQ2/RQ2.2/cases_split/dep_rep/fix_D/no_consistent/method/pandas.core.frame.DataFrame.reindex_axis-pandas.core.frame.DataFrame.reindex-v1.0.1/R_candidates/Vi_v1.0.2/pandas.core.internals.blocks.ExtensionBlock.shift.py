    def shift(
        self, periods: int, axis: int = 0, fill_value: Any = None,
    ) -> List["ExtensionBlock"]:
        """
        Shift the block by `periods`.

        Dispatches to underlying ExtensionArray and re-boxes in an
        ExtensionBlock.
        """
        return [
            self.make_block_same_class(
                self.values.shift(periods=periods, fill_value=fill_value),
                placement=self.mgr_locs,
                ndim=self.ndim,
            )
        ]
