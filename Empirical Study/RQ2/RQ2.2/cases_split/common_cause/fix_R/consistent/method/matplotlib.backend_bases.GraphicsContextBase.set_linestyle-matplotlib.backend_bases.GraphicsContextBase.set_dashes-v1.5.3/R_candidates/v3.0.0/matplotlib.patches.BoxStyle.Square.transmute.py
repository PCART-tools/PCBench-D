        def transmute(self, x0, y0, width, height, mutation_size):
            pad = mutation_size * self.pad

            # width and height with padding added.
            width, height = width + 2*pad, height + 2*pad

            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad,
            x1, y1 = x0 + width, y0 + height

            vertices = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
            codes = [Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY]
            return Path(vertices, codes)
