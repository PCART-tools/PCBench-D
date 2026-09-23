    def edit_right_margin_min(self, margin):
        self.solver.suggestValue(self.right_margin_min, margin)
