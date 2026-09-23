    def set_radius(self, radius):
        """
        Set the radius of the circle

        ACCEPTS: float
        """
        self.width = self.height = 2 * radius
        self.stale = True
