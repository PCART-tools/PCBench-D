        def _get_sawtooth_vertices(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # size of sawtooth
            if self.tooth_size is None:
                tooth_size = self.pad * .5 * mutation_size
            else:
                tooth_size = self.tooth_size * mutation_size

            hsz = tooth_size / 2
            width = width + 2 * pad - tooth_size
            height = height + 2 * pad - tooth_size

            # the sizes of the vertical and horizontal sawtooth are
            # separately adjusted to fit the given box size.
            dsx_n = round((width - tooth_size) / (tooth_size * 2)) * 2
            dsx = (width - tooth_size) / dsx_n
            dsy_n = round((height - tooth_size) / (tooth_size * 2)) * 2
            dsy = (height - tooth_size) / dsy_n

            x0, y0 = x0 - pad + hsz, y0 - pad + hsz
            x1, y1 = x0 + width, y0 + height

            xs = [
                x0, *np.linspace(x0 + hsz, x1 - hsz, 2 * dsx_n + 1),  # bottom
                *([x1, x1 + hsz, x1, x1 - hsz] * dsy_n)[:2*dsy_n+2],  # right
                x1, *np.linspace(x1 - hsz, x0 + hsz, 2 * dsx_n + 1),  # top
                *([x0, x0 - hsz, x0, x0 + hsz] * dsy_n)[:2*dsy_n+2],  # left
            ]
            ys = [
                *([y0, y0 - hsz, y0, y0 + hsz] * dsx_n)[:2*dsx_n+2],  # bottom
                y0, *np.linspace(y0 + hsz, y1 - hsz, 2 * dsy_n + 1),  # right
                *([y1, y1 + hsz, y1, y1 - hsz] * dsx_n)[:2*dsx_n+2],  # top
                y1, *np.linspace(y1 - hsz, y0 + hsz, 2 * dsy_n + 1),  # left
            ]

            return [*zip(xs, ys), (xs[0], ys[0])]
