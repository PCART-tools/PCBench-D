    def constrain_bottom(self, bottom, strength='strong'):
        c = (self.bottom == bottom)
        self.solver.addConstraint(c | strength)
