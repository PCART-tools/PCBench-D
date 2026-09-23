    def constrain_left_margin(self, margin, strength='strong'):
        c = (self.left == self.parent.left + margin)
        self.solver.addConstraint(c | strength)
