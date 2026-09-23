    def _maybe_downcast(self, blocks, downcast=None):

        if downcast is not None:
            return blocks

        # split and convert the blocks
        return _extend_blocks([b.convert(datetime=True, numeric=False)
                               for b in blocks])
