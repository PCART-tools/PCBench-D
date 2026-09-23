    def constrain_right(self, right, strength='strong'):
        c = (self.right == right)
        self.solver.addConstraint(c | strength)
