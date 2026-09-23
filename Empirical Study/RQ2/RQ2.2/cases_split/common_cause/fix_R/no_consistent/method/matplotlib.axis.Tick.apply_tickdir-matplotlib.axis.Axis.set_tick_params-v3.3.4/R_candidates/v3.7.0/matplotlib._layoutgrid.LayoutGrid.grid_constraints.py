    def grid_constraints(self):
        # constrain the ratio of the inner part of the grids
        # to be the same (relative to width_ratios)

        # constrain widths:
        w = (self.rights[0] - self.margins['right'][0] -
             self.margins['rightcb'][0])
        w = (w - self.lefts[0] - self.margins['left'][0] -
             self.margins['leftcb'][0])
        w0 = w / self.width_ratios[0]
        # from left to right
        for i in range(1, self.ncols):
            w = (self.rights[i] - self.margins['right'][i] -
                 self.margins['rightcb'][i])
            w = (w - self.lefts[i] - self.margins['left'][i] -
                 self.margins['leftcb'][i])
            c = (w == w0 * self.width_ratios[i])
            self.solver.addConstraint(c | 'strong')
            # constrain the grid cells to be directly next to each other.
            c = (self.rights[i - 1] == self.lefts[i])
            self.solver.addConstraint(c | 'strong')

        # constrain heights:
        h = self.tops[0] - self.margins['top'][0] - self.margins['topcb'][0]
        h = (h - self.bottoms[0] - self.margins['bottom'][0] -
             self.margins['bottomcb'][0])
        h0 = h / self.height_ratios[0]
        # from top to bottom:
        for i in range(1, self.nrows):
            h = (self.tops[i] - self.margins['top'][i] -
                 self.margins['topcb'][i])
            h = (h - self.bottoms[i] - self.margins['bottom'][i] -
                 self.margins['bottomcb'][i])
            c = (h == h0 * self.height_ratios[i])
            self.solver.addConstraint(c | 'strong')
            # constrain the grid cells to be directly above each other.
            c = (self.bottoms[i - 1] == self.tops[i])
            self.solver.addConstraint(c | 'strong')
