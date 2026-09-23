    def _maybe_downcast(self, blocks, downcast=None):

        # no need to downcast our float
        # unless indicated
        if downcast is None and self.is_float:
            return blocks
        elif downcast is None and (self.is_timedelta or self.is_datetime):
            return blocks

        if not isinstance(blocks, list):
            blocks = [blocks]
        return _extend_blocks([b.downcast(downcast) for b in blocks])
