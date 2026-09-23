    def get_topmost_subplotspec(self):
        'get the topmost SubplotSpec instance associated with the subplot'
        gridspec = self.get_gridspec()
        if hasattr(gridspec, "get_topmost_subplotspec"):
            return gridspec.get_topmost_subplotspec()
        else:
            return self
