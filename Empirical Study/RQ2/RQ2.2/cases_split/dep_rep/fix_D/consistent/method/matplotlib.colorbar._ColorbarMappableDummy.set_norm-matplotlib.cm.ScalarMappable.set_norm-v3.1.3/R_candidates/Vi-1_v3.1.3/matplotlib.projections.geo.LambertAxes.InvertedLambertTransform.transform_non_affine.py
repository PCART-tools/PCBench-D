        def transform_non_affine(self, xy):
            # docstring inherited
            x = xy[:, 0:1]
            y = xy[:, 1:2]
            clong = self._center_longitude
            clat = self._center_latitude
            p = np.maximum(np.hypot(x, y), 1e-9)
            c = 2 * np.arcsin(0.5 * p)
            sin_c = np.sin(c)
            cos_c = np.cos(c)

            lat = np.arcsin(cos_c*np.sin(clat) +
                             ((y*sin_c*np.cos(clat)) / p))
            lon = clong + np.arctan(
                (x*sin_c) / (p*np.cos(clat)*cos_c - y*np.sin(clat)*sin_c))

            return np.concatenate((lon, lat), 1)
