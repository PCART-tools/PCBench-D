        def transform_non_affine(self, ll):
            def d(theta):
                delta = -(theta + np.sin(theta) - pi_sin_l) / (1 + np.cos(theta))
                return delta, np.abs(delta) > 0.001

            longitude = ll[:, 0]
            latitude  = ll[:, 1]

            clat = np.pi/2 - np.abs(latitude)
            ihigh = clat < 0.087 # within 5 degrees of the poles
            ilow = ~ihigh
            aux = np.empty(latitude.shape, dtype=float)

            if ilow.any():  # Newton-Raphson iteration
                pi_sin_l = np.pi * np.sin(latitude[ilow])
                theta = 2.0 * latitude[ilow]
                delta, large_delta = d(theta)
                while np.any(large_delta):
                    theta[large_delta] += delta[large_delta]
                    delta, large_delta = d(theta)
                aux[ilow] = theta / 2

            if ihigh.any(): # Taylor series-based approx. solution
                e = clat[ihigh]
                d = 0.5 * (3 * np.pi * e**2) ** (1.0/3)
                aux[ihigh] = (np.pi/2 - d) * np.sign(latitude[ihigh])

            xy = np.empty(ll.shape, dtype=float)
            xy[:,0] = (2.0 * np.sqrt(2.0) / np.pi) * longitude * np.cos(aux)
            xy[:,1] = np.sqrt(2.0) * np.sin(aux)

            return xy
