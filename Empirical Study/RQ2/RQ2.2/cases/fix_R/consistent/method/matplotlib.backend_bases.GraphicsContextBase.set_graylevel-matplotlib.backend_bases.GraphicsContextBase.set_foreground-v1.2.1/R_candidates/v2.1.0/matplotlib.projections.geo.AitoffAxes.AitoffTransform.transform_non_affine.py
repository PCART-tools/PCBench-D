        def transform_non_affine(self, ll):
            longitude = ll[:, 0:1]
            latitude  = ll[:, 1:2]

            # Pre-compute some values
            half_long = longitude / 2.0
            cos_latitude = np.cos(latitude)

            alpha = np.arccos(cos_latitude * np.cos(half_long))
            # Mask this array or we'll get divide-by-zero errors
            alpha = ma.masked_where(alpha == 0.0, alpha)
            # The numerators also need to be masked so that masked
            # division will be invoked.
            # We want unnormalized sinc.  numpy.sinc gives us normalized
            sinc_alpha = ma.sin(alpha) / alpha

            x = (cos_latitude * ma.sin(half_long)) / sinc_alpha
            y = (ma.sin(latitude) / sinc_alpha)
            return np.concatenate((x.filled(0), y.filled(0)), 1)
