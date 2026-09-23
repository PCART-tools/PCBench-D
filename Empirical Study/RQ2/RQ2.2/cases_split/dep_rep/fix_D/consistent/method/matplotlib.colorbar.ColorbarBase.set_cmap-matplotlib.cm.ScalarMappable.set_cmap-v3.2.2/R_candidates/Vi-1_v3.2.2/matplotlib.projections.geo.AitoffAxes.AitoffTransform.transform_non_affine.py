        def transform_non_affine(self, ll):
            # docstring inherited
            longitude, latitude = ll.T

            # Pre-compute some values
            half_long = longitude / 2.0
            cos_latitude = np.cos(latitude)

            alpha = np.arccos(cos_latitude * np.cos(half_long))
            # Avoid divide-by-zero errors using same method as NumPy.
            alpha[alpha == 0.0] = 1e-20
            # We want unnormalized sinc.  numpy.sinc gives us normalized
            sinc_alpha = np.sin(alpha) / alpha

            x = (cos_latitude * np.sin(half_long)) / sinc_alpha
            y = np.sin(latitude) / sinc_alpha
            return np.column_stack([x, y])
