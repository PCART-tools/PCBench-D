    def edit_height(self, height, strength='strong'):
        """
        Set the height of the layout box.

        This is done as an editable variable so that the value can change
        due to resizing.
        """
        sol = self.solver
        for i in [self.height]:
            if not sol.hasEditVariable(i):
                sol.addEditVariable(i, strength)
        sol.suggestValue(self.height, height)
