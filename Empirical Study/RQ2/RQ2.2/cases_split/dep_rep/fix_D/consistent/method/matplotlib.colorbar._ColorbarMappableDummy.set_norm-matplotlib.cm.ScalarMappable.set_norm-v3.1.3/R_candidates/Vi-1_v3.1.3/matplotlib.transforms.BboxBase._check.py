        def _check(points):
            if isinstance(points, np.ma.MaskedArray):
                cbook._warn_external("Bbox bounds are a masked array.")
            points = np.asarray(points)
            if (points[1, 0] - points[0, 0] == 0 or
                points[1, 1] - points[0, 1] == 0):
                cbook._warn_external("Singular Bbox.")
