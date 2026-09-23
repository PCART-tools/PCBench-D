    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('*')) * density
        path = Path.unit_regular_star(5)
        self.shape_vertices = path.vertices
        self.shape_codes = np.ones(len(self.shape_vertices)) * Path.LINETO
        self.shape_codes[0] = Path.MOVETO
        Shapes.__init__(self, hatch, density)
