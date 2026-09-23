    def constrain_width(self, width, strength='strong'):
        """
        Constrain the width of the layout box.  *width* is
        either a float or a layoutbox.width.
        """
        c = (self.width == width)
        self.solver.addConstraint(c | strength)
