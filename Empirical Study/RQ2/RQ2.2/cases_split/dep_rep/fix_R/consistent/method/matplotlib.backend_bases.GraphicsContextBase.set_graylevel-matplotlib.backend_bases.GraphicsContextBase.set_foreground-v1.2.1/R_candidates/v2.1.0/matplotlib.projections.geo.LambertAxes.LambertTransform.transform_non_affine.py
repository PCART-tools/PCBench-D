        def transform_non_affine(self, ll):
            longitude = ll[:, 0:1]
            latitude  = ll[:, 1:2]
            clong = self._center_longitude
            clat = self._center_latitude
            cos_lat = np.cos(latitude)
            sin_lat = np.sin(latitude)
            diff_long = longitude - clong
            cos_diff_long = np.cos(diff_long)

            inner_k = (1.0 +
                       np.sin(clat)*sin_lat +
                       np.cos(clat)*cos_lat*cos_diff_long)
            # Prevent divide-by-zero problems
            inner_k = np.where(inner_k == 0.0, 1e-15, inner_k)
            k = np.sqrt(2.0 / inner_k)
            x = k*cos_lat*np.sin(diff_long)
            y = k*(np.cos(clat)*sin_lat -
                   np.sin(clat)*cos_lat*cos_diff_long)

            return np.concatenate((x, y), 1)
