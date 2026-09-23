    def constrain_top(self, top, strength='strong'):
        c = (self.top == top)
        self.solver.addConstraint(c | strength)
