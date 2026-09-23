        def __call__(self, x0, y0, width, height, mutation_size):
            # padding
            pad = mutation_size * self.pad
            # width and height with padding added.
            width, height = width + 2 * pad, height + 2 * pad
            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad,
            x1, y1 = x0 + width, y0 + height

            dx = (y1 - y0) / 2
            dxx = dx / 2
            x0 = x0 + pad / 1.4  # adjust by ~sqrt(2)

            return Path._create_closed(
                [(x0 + dxx, y0), (x1, y0), (x1, y1), (x0 + dxx, y1),
                 (x0 + dxx, y1 + dxx), (x0 - dx, y0 + dx),
                 (x0 + dxx, y0 - dxx),  # arrow
                 (x0 + dxx, y0)])
