    def _apply_loffset(self, result):
        """
        If loffset is set, offset the result index.

        This is NOT an idempotent routine, it will be applied
        exactly once to the result.

        Parameters
        ----------
        result : Series or DataFrame
            the result of resample
        """

        needs_offset = (
            isinstance(self.loffset, (DateOffset, timedelta, np.timedelta64))
            and isinstance(result.index, DatetimeIndex)
            and len(result.index) > 0
        )

        if needs_offset:
            result.index = result.index + self.loffset

        self.loffset = None
        return result
