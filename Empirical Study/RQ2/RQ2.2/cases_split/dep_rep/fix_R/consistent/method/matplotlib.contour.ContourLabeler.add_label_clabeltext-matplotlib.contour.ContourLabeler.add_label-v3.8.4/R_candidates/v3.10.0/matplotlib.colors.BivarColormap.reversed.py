    def reversed(self, axis_0=True, axis_1=True):
        """
        Reverses both or one of the axis.
        """
        r_0 = -1 if axis_0 else 1
        r_1 = -1 if axis_1 else 1
        return self.resampled((r_0, r_1))
