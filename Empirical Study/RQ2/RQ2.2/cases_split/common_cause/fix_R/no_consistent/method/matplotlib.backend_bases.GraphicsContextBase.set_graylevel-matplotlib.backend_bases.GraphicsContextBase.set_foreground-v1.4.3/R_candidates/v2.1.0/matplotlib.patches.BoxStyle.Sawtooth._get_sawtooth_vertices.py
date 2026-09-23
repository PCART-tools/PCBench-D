        def _get_sawtooth_vertices(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # size of sawtooth
            if self.tooth_size is None:
                tooth_size = self.pad * .5 * mutation_size
            else:
                tooth_size = self.tooth_size * mutation_size

            tooth_size2 = tooth_size / 2.
            width, height = (width + 2. * pad - tooth_size,
                            height + 2. * pad - tooth_size)

            # the sizes of the vertical and horizontal sawtooth are
            # separately adjusted to fit the given box size.
            dsx_n = int(np.round((width - tooth_size) / (tooth_size * 2))) * 2
            dsx = (width - tooth_size) / dsx_n
            dsy_n = int(np.round((height - tooth_size) / (tooth_size * 2))) * 2
            dsy = (height - tooth_size) / dsy_n

            x0, y0 = x0 - pad + tooth_size2, y0 - pad + tooth_size2
            x1, y1 = x0 + width, y0 + height

            bottom_saw_x = [x0] + \
                           [x0 + tooth_size2 + dsx * .5 * i
                            for i
                            in range(dsx_n * 2)] + \
                           [x1 - tooth_size2]

            bottom_saw_y = [y0] + \
                           [y0 - tooth_size2, y0,
                            y0 + tooth_size2, y0] * dsx_n + \
                           [y0 - tooth_size2]

            right_saw_x = [x1] + \
                          [x1 + tooth_size2,
                           x1,
                           x1 - tooth_size2,
                           x1] * dsx_n + \
                          [x1 + tooth_size2]

            right_saw_y = [y0] + \
                          [y0 + tooth_size2 + dsy * .5 * i
                           for i
                           in range(dsy_n * 2)] + \
                          [y1 - tooth_size2]

            top_saw_x = [x1] + \
                        [x1 - tooth_size2 - dsx * .5 * i
                         for i
                         in range(dsx_n * 2)] + \
                        [x0 + tooth_size2]

            top_saw_y = [y1] + \
                        [y1 + tooth_size2,
                         y1,
                         y1 - tooth_size2,
                         y1] * dsx_n + \
                        [y1 + tooth_size2]

            left_saw_x = [x0] + \
                         [x0 - tooth_size2,
                          x0,
                          x0 + tooth_size2,
                          x0] * dsy_n + \
                         [x0 - tooth_size2]

            left_saw_y = [y1] + \
                         [y1 - tooth_size2 - dsy * .5 * i
                          for i
                          in range(dsy_n * 2)] + \
                         [y0 + tooth_size2]

            saw_vertices = (list(zip(bottom_saw_x, bottom_saw_y)) +
                            list(zip(right_saw_x, right_saw_y)) +
                            list(zip(top_saw_x, top_saw_y)) +
                            list(zip(left_saw_x, left_saw_y)) +
                            [(bottom_saw_x[0], bottom_saw_y[0])])

            return saw_vertices
