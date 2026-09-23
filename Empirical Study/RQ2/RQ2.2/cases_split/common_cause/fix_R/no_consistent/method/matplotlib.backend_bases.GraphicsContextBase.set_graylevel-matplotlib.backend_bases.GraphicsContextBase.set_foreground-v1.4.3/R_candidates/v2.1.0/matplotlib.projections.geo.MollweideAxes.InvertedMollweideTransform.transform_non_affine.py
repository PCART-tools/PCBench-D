        def transform_non_affine(self, xy):
            x = xy[:, 0:1]
            y = xy[:, 1:2]

            # from Equations (7, 8) of
            # http://mathworld.wolfram.com/MollweideProjection.html
            theta = np.arcsin(y / np.sqrt(2))
            lon = (np.pi / (2 * np.sqrt(2))) * x / np.cos(theta)
            lat = np.arcsin((2 * theta + np.sin(2 * theta)) / np.pi)

            return np.concatenate((lon, lat), 1)
