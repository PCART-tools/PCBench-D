    def edit_top_margin_min(self, margin):
        self.solver.suggestValue(self.top_margin_min, margin)
