        @staticmethod
        def _check(points):
            if isinstance(points, np.ma.MaskedArray):
                _api.warn_external("Bbox bounds are a masked array.")
            points = np.asarray(points)
            if any((points[1, :] - points[0, :]) == 0):
                _api.warn_external("Singular Bbox.")
