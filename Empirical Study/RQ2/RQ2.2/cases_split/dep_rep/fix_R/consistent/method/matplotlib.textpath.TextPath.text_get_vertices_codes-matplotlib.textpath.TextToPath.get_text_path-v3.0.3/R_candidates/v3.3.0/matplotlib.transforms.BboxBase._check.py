        @staticmethod
        def _check(points):
            if isinstance(points, np.ma.MaskedArray):
                cbook._warn_external("Bbox bounds are a masked array.")
            points = np.asarray(points)
            if any((points[1, :] - points[0, :]) == 0):
                cbook._warn_external("Singular Bbox.")
