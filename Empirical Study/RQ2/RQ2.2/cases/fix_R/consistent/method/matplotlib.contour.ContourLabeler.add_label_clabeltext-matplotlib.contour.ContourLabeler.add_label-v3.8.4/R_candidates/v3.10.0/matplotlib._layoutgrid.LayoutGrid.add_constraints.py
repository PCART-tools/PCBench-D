    def add_constraints(self, parent):
        # define self-consistent constraints
        self.hard_constraints()
        # define relationship with parent layoutgrid:
        self.parent_constraints(parent)
        # define relative widths of the grid cells to each other
        # and stack horizontally and vertically.
        self.grid_constraints()
