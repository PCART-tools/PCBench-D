    @_register_style(_style_list)
    class Sawtooth(_Base):
        """A box with a sawtooth outline."""

        def __init__(self, pad=0.3, tooth_size=None):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            tooth_size : float, default: *pad*/2
                Size of the sawtooth.
            """
            self.pad = pad
            self.tooth_size = tooth_size

        def _get_sawtooth_vertices(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # size of sawtooth
            if self.tooth_size is None:
                tooth_size = self.pad * .5 * mutation_size
            else:
                tooth_size = self.tooth_size * mutation_size

            tooth_size2 = tooth_size / 2
            width = width + 2 * pad - tooth_size
            height = height + 2 * pad - tooth_size

            # the sizes of the vertical and horizontal sawtooth are
            # separately adjusted to fit the given box size.
            dsx_n = int(round((width - tooth_size) / (tooth_size * 2))) * 2
            dsx = (width - tooth_size) / dsx_n
            dsy_n = int(round((height - tooth_size) / (tooth_size * 2))) * 2
            dsy = (height - tooth_size) / dsy_n

            x0, y0 = x0 - pad + tooth_size2, y0 - pad + tooth_size2
            x1, y1 = x0 + width, y0 + height

            bottom_saw_x = [
                x0,
                *(x0 + tooth_size2 + dsx * .5 * np.arange(dsx_n * 2)),
                x1 - tooth_size2,
            ]
            bottom_saw_y = [
                y0,
                *([y0 - tooth_size2, y0, y0 + tooth_size2, y0] * dsx_n),
                y0 - tooth_size2,
            ]
            right_saw_x = [
                x1,
                *([x1 + tooth_size2, x1, x1 - tooth_size2, x1] * dsx_n),
                x1 + tooth_size2,
            ]
            right_saw_y = [
                y0,
                *(y0 + tooth_size2 + dsy * .5 * np.arange(dsy_n * 2)),
                y1 - tooth_size2,
            ]
            top_saw_x = [
                x1,
                *(x1 - tooth_size2 - dsx * .5 * np.arange(dsx_n * 2)),
                x0 + tooth_size2,
            ]
            top_saw_y = [
                y1,
                *([y1 + tooth_size2, y1, y1 - tooth_size2, y1] * dsx_n),
                y1 + tooth_size2,
            ]
            left_saw_x = [
                x0,
                *([x0 - tooth_size2, x0, x0 + tooth_size2, x0] * dsy_n),
                x0 - tooth_size2,
            ]
            left_saw_y = [
                y1,
                *(y1 - tooth_size2 - dsy * .5 * np.arange(dsy_n * 2)),
                y0 + tooth_size2,
            ]

            saw_vertices = [*zip(bottom_saw_x, bottom_saw_y),
                            *zip(right_saw_x, right_saw_y),
                            *zip(top_saw_x, top_saw_y),
                            *zip(left_saw_x, left_saw_y),
                            (bottom_saw_x[0], bottom_saw_y[0])]

            return saw_vertices

        def __call__(self, x0, y0, width, height, mutation_size):
            saw_vertices = self._get_sawtooth_vertices(x0, y0, width,
                                                       height, mutation_size)
            path = Path(saw_vertices, closed=True)
            return path
