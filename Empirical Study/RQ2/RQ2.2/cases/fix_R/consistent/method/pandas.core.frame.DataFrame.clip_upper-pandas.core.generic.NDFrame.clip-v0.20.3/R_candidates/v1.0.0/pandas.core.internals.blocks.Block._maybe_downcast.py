    def _maybe_downcast(self, blocks: List["Block"], downcast=None) -> List["Block"]:

        # no need to downcast our float
        # unless indicated
        if downcast is None and (
            self.is_float or self.is_timedelta or self.is_datetime
        ):
            return blocks

        return _extend_blocks([b.downcast(downcast) for b in blocks])
