    def constrain_width_min(self, width, strength='strong'):
        c = (self.width >= width)
        self.solver.addConstraint(c | strength)
