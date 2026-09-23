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
                cols = np.linspace(0.0, 1.0, self.num_rows + 1, True)
            else:
                cols = np.linspace(offset / 2.0, 1.0 - offset / 2.0,
                                   self.num_rows, True)
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
