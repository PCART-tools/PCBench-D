    def _maybe_downcast(self, blocks, downcast=None):

        # no need to downcast our float
        # unless indicated
        if downcast is None and self.is_float:
            return blocks
        elif downcast is None and (self.is_timedelta or self.is_datetime):
            return blocks

        result_blocks = []
        for b in blocks:
            result_blocks.extend(b.downcast(downcast))

        return result_blocks
