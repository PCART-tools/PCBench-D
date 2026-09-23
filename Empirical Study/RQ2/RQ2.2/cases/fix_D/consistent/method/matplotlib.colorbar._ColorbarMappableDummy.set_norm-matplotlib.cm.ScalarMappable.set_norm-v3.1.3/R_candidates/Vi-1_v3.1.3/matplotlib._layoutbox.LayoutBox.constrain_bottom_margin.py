    def constrain_bottom_margin(self, margin, strength='strong'):
        c = (self.bottom == self.parent.bottom + margin)
        self.solver.addConstraint(c | strength)
