    def get_path(self):
        # Since this is dpi dependent, we need to recompute the path
        # every time.

        # the base vertices
        x1, y1 = self.xytip
        x2, y2 = self.xybase
        k1 = self.width * self.figure.dpi / 72. / 2.
        k2 = self.headwidth * self.figure.dpi / 72. / 2.
        xb1, yb1, xb2, yb2 = self.getpoints(x1, y1, x2, y2, k1)

        # a point on the segment 20% of the distance from the tip to the base
        theta = math.atan2(y2 - y1, x2 - x1)
        r = math.sqrt((y2 - y1) ** 2. + (x2 - x1) ** 2.)
        xm = x1 + self.frac * r * math.cos(theta)
        ym = y1 + self.frac * r * math.sin(theta)
        xc1, yc1, xc2, yc2 = self.getpoints(x1, y1, xm, ym, k1)
        xd1, yd1, xd2, yd2 = self.getpoints(x1, y1, xm, ym, k2)

        xs = self.convert_xunits([xb1, xb2, xc2, xd2, x1, xd1, xc1, xb1])
        ys = self.convert_yunits([yb1, yb2, yc2, yd2, y1, yd1, yc1, yb1])

        return Path(np.column_stack([xs, ys]), closed=True)
