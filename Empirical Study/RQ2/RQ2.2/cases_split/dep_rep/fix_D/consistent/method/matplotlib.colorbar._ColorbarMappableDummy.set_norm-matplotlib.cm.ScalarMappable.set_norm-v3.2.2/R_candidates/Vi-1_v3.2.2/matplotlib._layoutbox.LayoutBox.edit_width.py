    def edit_width(self, width, strength='strong'):
        sol = self.solver
        for i in [self.width]:
            if not sol.hasEditVariable(i):
                sol.addEditVariable(i, strength)
        sol.suggestValue(self.width, width)
