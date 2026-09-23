    def constrain_margins(self):
        """
        Only do this for pos.  This sets a variable distance
        margin between the position of the axes and the outer edge of
        the axes.

        Margins are variable because they change with the fogure size.

        Margin minimums are set to make room for axes decorations.  However,
        the margins can be larger if we are mathicng the position size to
        otehr axes.
        """
        sol = self.solver

        # left
        if not sol.hasEditVariable(self.left_margin_min):
            sol.addEditVariable(self.left_margin_min, 'strong')
            sol.suggestValue(self.left_margin_min, 0.0001)
        c = (self.left_margin == self.left - self.parent.left)
        self.solver.addConstraint(c | 'required')
        c = (self.left_margin >= self.left_margin_min)
        self.solver.addConstraint(c | 'strong')

        # right
        if not sol.hasEditVariable(self.right_margin_min):
            sol.addEditVariable(self.right_margin_min, 'strong')
            sol.suggestValue(self.right_margin_min, 0.0001)
        c = (self.right_margin == self.parent.right - self.right)
        self.solver.addConstraint(c | 'required')
        c = (self.right_margin >= self.right_margin_min)
        self.solver.addConstraint(c | 'required')
        # bottom
        if not sol.hasEditVariable(self.bottom_margin_min):
            sol.addEditVariable(self.bottom_margin_min, 'strong')
            sol.suggestValue(self.bottom_margin_min, 0.0001)
        c = (self.bottom_margin == self.bottom - self.parent.bottom)
        self.solver.addConstraint(c | 'required')
        c = (self.bottom_margin >= self.bottom_margin_min)
        self.solver.addConstraint(c | 'required')
        # top
        if not sol.hasEditVariable(self.top_margin_min):
            sol.addEditVariable(self.top_margin_min, 'strong')
            sol.suggestValue(self.top_margin_min, 0.0001)
        c = (self.top_margin == self.parent.top - self.top)
        self.solver.addConstraint(c | 'required')
        c = (self.top_margin >= self.top_margin_min)
        self.solver.addConstraint(c | 'required')
