    def add_constraints(self):
        sol = self.solver
        # never let width and height go negative.
        for i in [self.min_width, self.min_height]:
            sol.addEditVariable(i, 1e9)
            sol.suggestValue(i, 0.0)
        # define relation ships between things thing width and right and left
        self.hard_constraints()
        # self.soft_constraints()
        if self.parent:
            self.parent_constrain()
