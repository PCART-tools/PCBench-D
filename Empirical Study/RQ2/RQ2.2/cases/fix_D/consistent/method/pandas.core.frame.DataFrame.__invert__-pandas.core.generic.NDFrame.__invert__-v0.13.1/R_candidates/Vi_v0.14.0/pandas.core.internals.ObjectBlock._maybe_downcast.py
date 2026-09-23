    def _maybe_downcast(self, blocks, downcast=None):

        if downcast is not None:
            return blocks

        # split and convert the blocks
        result_blocks = []
        for blk in blocks:
            result_blocks.extend(blk.convert(convert_dates=True,
                                             convert_numeric=False))
        return result_blocks
