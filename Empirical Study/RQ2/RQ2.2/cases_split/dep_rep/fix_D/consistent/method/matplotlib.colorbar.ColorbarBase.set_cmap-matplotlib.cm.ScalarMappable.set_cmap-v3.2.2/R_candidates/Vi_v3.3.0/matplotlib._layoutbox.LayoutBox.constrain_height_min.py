    def constrain_height_min(self, height, strength='strong'):
        c = (self.height >= height)
        self.solver.addConstraint(c | strength)
