    def find_nearest_contour(self, x, y, indices=None, pixel=True):
        """
        Finds contour that is closest to a point.  Defaults to
        measuring distance in pixels (screen space - useful for manual
        contour labeling), but this can be controlled via a keyword
        argument.

        Returns a tuple containing the contour, segment, index of
        segment, x & y of segment point and distance to minimum point.

        Optional keyword arguments:

          *indices*:
            Indexes of contour levels to consider when looking for
            nearest point.  Defaults to using all levels.

          *pixel*:
            If *True*, measure distance in pixel space, if not, measure
            distance in axes space.  Defaults to *True*.

        """

        # This function uses a method that is probably quite
        # inefficient based on converting each contour segment to
        # pixel coordinates and then comparing the given point to
        # those coordinates for each contour.  This will probably be
        # quite slow for complex contours, but for normal use it works
        # sufficiently well that the time is not noticeable.
        # Nonetheless, improvements could probably be made.

        if indices is None:
            indices = list(range(len(self.levels)))

        dmin = np.inf
        conmin = None
        segmin = None
        xmin = None
        ymin = None

        point = np.array([x, y])

        for icon in indices:
            con = self.collections[icon]
            trans = con.get_transform()
            paths = con.get_paths()

            for segNum, linepath in enumerate(paths):
                lc = linepath.vertices
                # transfer all data points to screen coordinates if desired
                if pixel:
                    lc = trans.transform(lc)

                d, xc, leg = _find_closest_point_on_path(lc, point)
                if d < dmin:
                    dmin = d
                    conmin = icon
                    segmin = segNum
                    imin = leg[1]
                    xmin = xc[0]
                    ymin = xc[1]

        return (conmin, segmin, imin, xmin, ymin, dmin)
