    def parent_constrain(self):
        parent = self.parent
        hc = [self.left >= parent.left,
              self.bottom >= parent.bottom,
              self.top <= parent.top,
              self.right <= parent.right]
        for c in hc:
            self.solver.addConstraint(c | 'required')
