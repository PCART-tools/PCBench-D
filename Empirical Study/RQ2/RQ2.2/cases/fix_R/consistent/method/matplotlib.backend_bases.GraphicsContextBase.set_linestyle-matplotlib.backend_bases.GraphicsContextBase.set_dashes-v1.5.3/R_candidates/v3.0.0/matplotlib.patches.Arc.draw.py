    @artist.allow_rasterization
    def draw(self, renderer):
        """
        Ellipses are normally drawn using an approximation that uses
        eight cubic Bezier splines.  The error of this approximation
        is 1.89818e-6, according to this unverified source:

          Lancaster, Don.  Approximating a Circle or an Ellipse Using
          Four Bezier Cubic Splines.

          http://www.tinaja.com/glib/ellipse4.pdf

        There is a use case where very large ellipses must be drawn
        with very high accuracy, and it is too expensive to render the
        entire ellipse with enough segments (either splines or line
        segments).  Therefore, in the case where either radius of the
        ellipse is large enough that the error of the spline
        approximation will be visible (greater than one pixel offset
        from the ideal), a different technique is used.

        In that case, only the visible parts of the ellipse are drawn,
        with each visible arc using a fixed number of spline segments
        (8).  The algorithm proceeds as follows:

          1. The points where the ellipse intersects the axes bounding
             box are located.  (This is done be performing an inverse
             transformation on the axes bbox such that it is relative
             to the unit circle -- this makes the intersection
             calculation much easier than doing rotated ellipse
             intersection directly).

             This uses the "line intersecting a circle" algorithm
             from:

               Vince, John.  Geometry for Computer Graphics: Formulae,
               Examples & Proofs.  London: Springer-Verlag, 2005.

          2. The angles of each of the intersection points are
             calculated.

          3. Proceeding counterclockwise starting in the positive
             x-direction, each of the visible arc-segments between the
             pairs of vertices are drawn using the Bezier arc
             approximation technique implemented in
             :meth:`matplotlib.path.Path.arc`.
        """
        if not hasattr(self, 'axes'):
            raise RuntimeError('Arcs can only be used in Axes instances')

        self._recompute_transform()

        width = self.convert_xunits(self.width)
        height = self.convert_yunits(self.height)

        # If the width and height of ellipse are not equal, take into account
        # stretching when calculating angles to draw between
        def theta_stretch(theta, scale):
            theta = np.deg2rad(theta)
            x = np.cos(theta)
            y = np.sin(theta)
            return np.rad2deg(np.arctan2(scale * y, x))
        theta1 = theta_stretch(self.theta1, width / height)
        theta2 = theta_stretch(self.theta2, width / height)

        # Get width and height in pixels
        width, height = self.get_transform().transform_point((width, height))
        inv_error = (1.0 / 1.89818e-6) * 0.5
        if width < inv_error and height < inv_error:
            self._path = Path.arc(theta1, theta2)
            return Patch.draw(self, renderer)

        def iter_circle_intersect_on_line(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            dr2 = dx * dx + dy * dy
            D = x0 * y1 - x1 * y0
            D2 = D * D
            discrim = dr2 - D2

            # Single (tangential) intersection
            if discrim == 0.0:
                x = (D * dy) / dr2
                y = (-D * dx) / dr2
                yield x, y
            elif discrim > 0.0:
                # The definition of "sign" here is different from
                # np.sign: we never want to get 0.0
                if dy < 0.0:
                    sign_dy = -1.0
                else:
                    sign_dy = 1.0
                sqrt_discrim = np.sqrt(discrim)
                for sign in (1., -1.):
                    x = (D * dy + sign * sign_dy * dx * sqrt_discrim) / dr2
                    y = (-D * dx + sign * np.abs(dy) * sqrt_discrim) / dr2
                    yield x, y

        def iter_circle_intersect_on_line_seg(x0, y0, x1, y1):
            epsilon = 1e-9
            if x1 < x0:
                x0e, x1e = x1, x0
            else:
                x0e, x1e = x0, x1
            if y1 < y0:
                y0e, y1e = y1, y0
            else:
                y0e, y1e = y0, y1
            x0e -= epsilon
            y0e -= epsilon
            x1e += epsilon
            y1e += epsilon
            for x, y in iter_circle_intersect_on_line(x0, y0, x1, y1):
                if x0e <= x <= x1e and y0e <= y <= y1e:
                    yield x, y

        # Transforms the axes box_path so that it is relative to the unit
        # circle in the same way that it is relative to the desired
        # ellipse.
        box_path = Path.unit_rectangle()
        box_path_transform = transforms.BboxTransformTo(self.axes.bbox) + \
            self.get_transform().inverted()
        box_path = box_path.transformed(box_path_transform)

        thetas = set()
        # For each of the point pairs, there is a line segment
        for p0, p1 in zip(box_path.vertices[:-1], box_path.vertices[1:]):
            x0, y0 = p0
            x1, y1 = p1
            for x, y in iter_circle_intersect_on_line_seg(x0, y0, x1, y1):
                theta = np.arccos(x)
                if y < 0:
                    theta = 2 * np.pi - theta
                # Convert radians to angles
                theta = np.rad2deg(theta)
                if theta1 < theta < theta2:
                    thetas.add(theta)
        thetas = sorted(thetas) + [theta2]

        last_theta = theta1
        theta1_rad = np.deg2rad(theta1)
        inside = box_path.contains_point((np.cos(theta1_rad),
                                          np.sin(theta1_rad)))

        # save original path
        path_original = self._path
        for theta in thetas:
            if inside:
                self._path = Path.arc(last_theta, theta, 8)
                Patch.draw(self, renderer)
                inside = False
            else:
                inside = True
            last_theta = theta

        # restore original path
        self._path = path_original
