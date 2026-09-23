    def _adjust_binner_for_upsample(self, binner):
        """
        Adjust our binner when upsampling.

        The range of a new index should not be outside specified range
        """
        if self.closed == 'right':
            binner = binner[1:]
        else:
            binner = binner[:-1]
        return binner
