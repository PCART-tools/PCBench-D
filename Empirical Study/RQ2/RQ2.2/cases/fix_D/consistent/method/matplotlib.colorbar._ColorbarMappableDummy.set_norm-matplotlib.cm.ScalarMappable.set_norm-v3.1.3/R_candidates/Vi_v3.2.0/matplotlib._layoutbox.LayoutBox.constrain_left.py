    def constrain_left(self, left,  strength='strong'):
        c = (self.left == left)
        self.solver.addConstraint(c | strength)
