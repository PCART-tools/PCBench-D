    def constrain_right_margin(self, margin, strength='strong'):
        c = (self.right == self.parent.right - margin)
        self.solver.addConstraint(c | strength)
