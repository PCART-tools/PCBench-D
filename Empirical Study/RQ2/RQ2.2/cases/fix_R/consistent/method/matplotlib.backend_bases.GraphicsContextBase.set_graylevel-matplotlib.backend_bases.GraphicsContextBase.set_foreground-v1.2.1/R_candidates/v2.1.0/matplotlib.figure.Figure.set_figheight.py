    def set_figheight(self, val, forward=False):
        """
        Set the height of the figure in inches

        ACCEPTS: float
        """
        self.set_size_inches(self.get_figwidth(), val, forward=forward)
