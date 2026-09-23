    def constrain_top_margin(self, margin, strength='strong'):
        c = (self.top == self.parent.top - margin)
        self.solver.addConstraint(c | strength)
