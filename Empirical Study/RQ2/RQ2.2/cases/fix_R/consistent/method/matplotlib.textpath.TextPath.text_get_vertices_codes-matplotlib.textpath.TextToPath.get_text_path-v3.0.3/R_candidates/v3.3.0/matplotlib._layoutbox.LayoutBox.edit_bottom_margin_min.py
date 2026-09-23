    def edit_bottom_margin_min(self, margin):
        self.solver.suggestValue(self.bottom_margin_min, margin)
