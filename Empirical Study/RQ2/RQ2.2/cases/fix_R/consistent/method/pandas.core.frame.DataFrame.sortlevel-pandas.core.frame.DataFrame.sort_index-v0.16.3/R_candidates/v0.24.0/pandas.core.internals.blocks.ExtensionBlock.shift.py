    def shift(self, periods, axis=0, fill_value=None):
        """
        Shift the block by `periods`.

        Dispatches to underlying ExtensionArray and re-boxes in an
        ExtensionBlock.
        """
        # type: (int, Optional[BlockPlacement]) -> List[ExtensionBlock]
        return [
            self.make_block_same_class(
                self.values.shift(periods=periods, fill_value=fill_value),
                placement=self.mgr_locs, ndim=self.ndim)
        ]
