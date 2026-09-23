    def set_xmargin(self, m):
        """
        Set padding of X data limits prior to autoscaling.

        *m* times the data interval will be added to each
        end of that interval before it is used in autoscaling.

        accepts: float in range 0 to 1
        """
        if m < 0 or m > 1:
            raise ValueError("margin must be in range 0 to 1")
        self._xmargin = m
        self.stale = True
