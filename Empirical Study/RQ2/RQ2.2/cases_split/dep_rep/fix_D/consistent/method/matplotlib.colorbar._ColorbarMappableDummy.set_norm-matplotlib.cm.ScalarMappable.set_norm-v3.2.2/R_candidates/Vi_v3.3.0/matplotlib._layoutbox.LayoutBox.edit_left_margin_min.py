    def edit_left_margin_min(self, margin):
        self.solver.suggestValue(self.left_margin_min, margin)
