    def hard_constraints(self):
        hc = [self.width == self.right - self.left,
              self.height == self.top - self.bottom,
              self.h_center == (self.left + self.right) * 0.5,
              self.v_center == (self.top + self.bottom) * 0.5,
              self.width >= self.min_width,
              self.height >= self.min_height]
        for c in hc:
            self.solver.addConstraint(c | 'required')
