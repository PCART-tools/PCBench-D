        def transmute(self, x0, y0, width, height, mutation_size):

            p = BoxStyle.LArrow.transmute(self, x0, y0,
                                          width, height, mutation_size)

            p.vertices[:, 0] = 2 * x0 + width - p.vertices[:, 0]

            return p
