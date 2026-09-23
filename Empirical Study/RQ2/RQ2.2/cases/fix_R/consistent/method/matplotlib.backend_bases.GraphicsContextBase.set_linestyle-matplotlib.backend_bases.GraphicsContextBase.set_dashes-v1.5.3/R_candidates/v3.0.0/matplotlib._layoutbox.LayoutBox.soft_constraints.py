    def soft_constraints(self):
        sol = self.solver
        if self.tightwidth:
            suggest = 0.
        else:
            suggest = 20.
        c = (self.pref_width == suggest)
        for i in c:
            sol.addConstraint(i | 'required')
        if self.tightheight:
            suggest = 0.
        else:
            suggest = 20.
        c = (self.pref_height == suggest)
        for i in c:
            sol.addConstraint(i | 'required')

        c = [(self.width >= suggest),
             (self.height >= suggest)]
        for i in c:
            sol.addConstraint(i | 150000)
