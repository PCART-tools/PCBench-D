    def set_pad(self, val):
        """
        Set the tick label pad in points

        ACCEPTS: float
        """
        self._apply_params(pad=val)
        self.stale = True
