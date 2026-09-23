    def getpoints(self, x1, y1, x2, y2, k):
        """
        For line segment defined by (*x1*, *y1*) and (*x2*, *y2*)
        return the points on the line that is perpendicular to the
        line and intersects (*x2*, *y2*) and the distance from (*x2*,
        *y2*) of the returned points is *k*.
        """
        x1, y1, x2, y2, k = map(float, (x1, y1, x2, y2, k))

        if y2 - y1 == 0:
            return x2, y2 + k, x2, y2 - k
        elif x2 - x1 == 0:
            return x2 + k, y2, x2 - k, y2

        m = (y2 - y1) / (x2 - x1)
        pm = -1. / m
        a = 1
        b = -2 * y2
        c = y2 ** 2. - k ** 2. * pm ** 2. / (1. + pm ** 2.)

        y3a = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        x3a = (y3a - y2) / pm + x2

        y3b = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        x3b = (y3b - y2) / pm + x2
        return x3a, y3a, x3b, y3b
