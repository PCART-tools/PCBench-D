    def constrain_geometry(self, left, bottom, right, top, strength='strong'):
        hc = [self.left == left,
              self.right == right,
              self.bottom == bottom,
              self.top == top]
        for c in hc:
            self.solver.addConstraint(c | strength)
