class HorizontalHatch(HatchPatternBase):
    def __init__(self, hatch, density):
        self.num_lines = int((hatch.count('-') + hatch.count('+')) * density)
        self.num_vertices = self.num_lines * 2

    def set_vertices_and_codes(self, vertices, codes):
        steps, stepsize = np.linspace(0.0, 1.0, self.num_lines, False,
                                      retstep=True)
        steps += stepsize / 2.
        vertices[0::2, 0] = 0.0
        vertices[0::2, 1] = steps
        vertices[1::2, 0] = 1.0
        vertices[1::2, 1] = steps
        codes[0::2] = Path.MOVETO
        codes[1::2] = Path.LINETO
