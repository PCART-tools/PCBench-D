    def _clip(self, X):
        """
        For internal use when applying a BivarColormap to data.
        i.e. cm.ScalarMappable().to_rgba()
        Clips X[0] and X[1] according to 'self.shape'.
        X is modified in-place.

        Parameters
        ----------
        X: np.array
            array of floats or ints to be clipped
        shape : {'square', 'circle', 'ignore', 'circleignore'}

            - If 'square' each variate is clipped to [0,1] independently
            - If 'circle' the variates are clipped radially to the center
              of the colormap.
              It is assumed that a circular mask is applied when the colormap
              is displayed
            - If 'ignore' the variates are not clipped, but instead assigned the
              'outside' color
            - If 'circleignore' a circular mask is applied, but the data is not clipped
              and instead assigned the 'outside' color

        """
        if self.shape == 'square':
            for X_part, mx in zip(X, (self.N, self.M)):
                X_part[X_part < 0] = 0
                if X_part.dtype.kind == "f":
                    X_part[X_part > 1] = 1
                else:
                    X_part[X_part >= mx] = mx - 1

        elif self.shape == 'ignore':
            for X_part, mx in zip(X, (self.N, self.M)):
                X_part[X_part < 0] = -1
                if X_part.dtype.kind == "f":
                    X_part[X_part > 1] = -1
                else:
                    X_part[X_part >= mx] = -1

        elif self.shape == 'circle' or self.shape == 'circleignore':
            for X_part in X:
                if X_part.dtype.kind != "f":
                    raise NotImplementedError(
                        "Circular bivariate colormaps are only"
                        " implemented for use with with floats")
            radii_sqr = (X[0] - 0.5)**2 + (X[1] - 0.5)**2
            mask_outside = radii_sqr > 0.25
            if self.shape == 'circle':
                overextend = 2 * np.sqrt(radii_sqr[mask_outside])
                X[0][mask_outside] = (X[0][mask_outside] - 0.5) / overextend + 0.5
                X[1][mask_outside] = (X[1][mask_outside] - 0.5) / overextend + 0.5
            else:
                X[0][mask_outside] = -1
                X[1][mask_outside] = -1
