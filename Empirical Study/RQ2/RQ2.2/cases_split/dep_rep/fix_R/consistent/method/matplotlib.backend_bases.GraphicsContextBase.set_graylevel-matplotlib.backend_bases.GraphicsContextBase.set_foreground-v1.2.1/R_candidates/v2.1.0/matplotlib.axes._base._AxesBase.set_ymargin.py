    def set_ymargin(self, m):
        """
        Set padding of Y data limits prior to autoscaling.

        *m* times the data interval will be added to each
        end of that interval before it is used in autoscaling.

        accepts: float in range 0 to 1
        """
        if m < 0 or m > 1:
            raise ValueError("margin must be in range 0 to 1")
        self._ymargin = m
        self.stale = True
