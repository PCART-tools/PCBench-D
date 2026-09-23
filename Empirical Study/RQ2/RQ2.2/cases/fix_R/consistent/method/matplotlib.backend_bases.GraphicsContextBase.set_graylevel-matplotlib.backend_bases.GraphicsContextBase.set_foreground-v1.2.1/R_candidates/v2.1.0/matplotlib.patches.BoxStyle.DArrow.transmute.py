        def transmute(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # width and height with padding added.
            # The width is padded by the arrows, so we don't need to pad it.
            height = height + 2. * pad

            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad
            x1, y1 = x0 + width, y0 + height

            dx = (y1 - y0)/2.
            dxx = dx * .5
            # adjust x0.  1.4 <- sqrt(2)
            x0 = x0 + pad / 1.4

            cp = [(x0 + dxx, y0), (x1, y0),  # bot-segment
                  (x1, y0 - dxx), (x1 + dx + dxx, y0 + dx),
                  (x1, y1 + dxx),  # right-arrow
                  (x1, y1), (x0 + dxx, y1),  # top-segment
                  (x0 + dxx, y1 + dxx), (x0 - dx, y0 + dx),
                  (x0 + dxx, y0 - dxx),  # left-arrow
                  (x0 + dxx, y0), (x0 + dxx, y0)]  # close-poly

            com = [Path.MOVETO, Path.LINETO,
                   Path.LINETO, Path.LINETO,
                   Path.LINETO,
                   Path.LINETO, Path.LINETO,
                   Path.LINETO, Path.LINETO,
                   Path.LINETO,
                   Path.LINETO, Path.CLOSEPOLY]

            path = Path(cp, com)

            return path
