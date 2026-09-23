    def constrain_same(self, other, strength='strong'):
        """
        Make the layoutbox have same position as other layoutbox
        """
        hc = [self.left == other.left,
              self.right == other.right,
              self.bottom == other.bottom,
              self.top == other.top]
        for c in hc:
            self.solver.addConstraint(c | strength)
