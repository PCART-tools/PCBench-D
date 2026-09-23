class Shapes(HatchPatternBase):
    filled = False

    def __init__(self, hatch, density):
        if self.num_rows == 0:
            self.num_shapes = 0
            self.num_vertices = 0
        else:
            self.num_shapes = ((self.num_rows // 2 + 1) * (self.num_rows + 1) +
                               (self.num_rows // 2) * self.num_rows)
            self.num_vertices = (self.num_shapes *
                                 len(self.shape_vertices) *
                                 (1 if self.filled else 2))

    def set_vertices_and_codes(self, vertices, codes):
        offset = 1.0 / self.num_rows
        shape_vertices = self.shape_vertices * offset * self.size
        if not self.filled:
            inner_vertices = shape_vertices[::-1] * 0.9
        shape_codes = self.shape_codes
        shape_size = len(shape_vertices)

        cursor = 0
        for row in range(self.num_rows + 1):
            if row % 2 == 0:
                cols = np.linspace(0, 1, self.num_rows + 1)
            else:
                cols = np.linspace(offset / 2, 1 - offset / 2, self.num_rows)
            row_pos = row * offset
            for col_pos in cols:
                vertices[cursor:cursor + shape_size] = (shape_vertices +
                                                        (col_pos, row_pos))
                codes[cursor:cursor + shape_size] = shape_codes
                cursor += shape_size
                if not self.filled:
                    vertices[cursor:cursor + shape_size] = (inner_vertices +
                                                            (col_pos, row_pos))
                    codes[cursor:cursor + shape_size] = shape_codes
                    cursor += shape_size
