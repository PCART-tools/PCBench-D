    @final
    def _maybe_downcast(self, blocks: list[Block], downcast=None) -> list[Block]:
        if downcast is False:
            return blocks

        if self.dtype == _dtype_obj:
            # GH#44241 We downcast regardless of the argument;
            #  respecting 'downcast=None' may be worthwhile at some point,
            #  but ATM it breaks too much existing code.
            # split and convert the blocks

            return extend_blocks(
                [blk.convert(datetime=True, numeric=False) for blk in blocks]
            )

        if downcast is None:
            return blocks

        return extend_blocks([b._downcast_2d(downcast) for b in blocks])
