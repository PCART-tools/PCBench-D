    def _verify_integrity(self) -> None:
        mgr_shape = self.shape
        tot_items = sum(len(x.mgr_locs) for x in self.blocks)
        for block in self.blocks:
            if block.shape[1:] != mgr_shape[1:]:
                raise construction_error(tot_items, block.shape[1:], self.axes)
        if len(self.items) != tot_items:
            raise AssertionError(
                "Number of manager items must equal union of "
                f"block items\n# manager items: {len(self.items)}, # "
                f"tot_items: {tot_items}"
            )
        if self.refs is not None:
            if len(self.refs) != len(self.blocks):
                raise AssertionError(
                    "Number of passed refs must equal the number of blocks: "
                    f"{len(self.refs)} refs vs {len(self.blocks)} blocks."
                    "\nIf you see this error, please report a bug at "
                    "https://github.com/pandas-dev/pandas/issues"
                )
