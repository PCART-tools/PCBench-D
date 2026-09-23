    def set_min(self, min):
        """
        Set the lower value of the slider to *min*.

        Parameters
        ----------
        min : float
        """
        self.set_val((min, self.val[1]))
