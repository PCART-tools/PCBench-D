        def __call__(self, x0, y0, width, height, mutation_size):
            pad = mutation_size * self.pad
            width, height = width + 2 * pad, height + 2 * pad
            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad
            a = width / math.sqrt(2)
            b = height / math.sqrt(2)
            trans = Affine2D().scale(a, b).translate(x0 + width / 2,
                                                     y0 + height / 2)
            return trans.transform_path(Path.unit_circle())
