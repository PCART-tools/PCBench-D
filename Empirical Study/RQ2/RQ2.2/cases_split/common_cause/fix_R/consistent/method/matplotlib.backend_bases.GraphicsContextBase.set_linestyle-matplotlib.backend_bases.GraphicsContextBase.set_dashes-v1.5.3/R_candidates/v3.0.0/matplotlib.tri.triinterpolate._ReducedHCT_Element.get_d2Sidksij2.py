    def get_d2Sidksij2(self, alpha, ecc):
        """
        Parameters
        ----------
        *alpha* is a (N x 3 x 1) array (array of column-matrices) of
        barycentric coordinates
        *ecc* is a (N x 3 x 1) array (array of column-matrices) of triangle
        eccentricities

        Returns
        -------
        Returns the arrays d2sdksi2 (N x 3 x 1) Hessian of shape functions
        expressed in covariante coordinates in first apex basis.
        """
        subtri = np.argmin(alpha, axis=1)[:, 0]
        ksi = _roll_vectorized(alpha, -subtri, axis=0)
        E = _roll_vectorized(ecc, -subtri, axis=0)
        x = ksi[:, 0, 0]
        y = ksi[:, 1, 0]
        z = ksi[:, 2, 0]
        d2V = _to_matrix_vectorized([
            [     6.*x,      6.*x,      6.*x],
            [     6.*y,        0.,        0.],
            [       0.,      6.*z,        0.],
            [     2.*z, 2.*z-4.*x, 2.*z-2.*x],
            [2.*y-4.*x,      2.*y, 2.*y-2.*x],
            [2.*x-4.*y,        0.,     -2.*y],
            [     2.*z,        0.,      2.*y],
            [       0.,      2.*y,      2.*z],
            [       0., 2.*x-4.*z,     -2.*z],
            [    -2.*z,     -2.*y,     x-y-z]])
        # Puts back d2V in first apex basis
        d2V = _prod_vectorized(d2V, _extract_submatrices(
            self.rotate_d2V, subtri, block_size=3, axis=0))
        prod = _prod_vectorized(self.M, d2V)
        prod += _scalar_vectorized(E[:, 0, 0],
                                   _prod_vectorized(self.M0, d2V))
        prod += _scalar_vectorized(E[:, 1, 0],
                                   _prod_vectorized(self.M1, d2V))
        prod += _scalar_vectorized(E[:, 2, 0],
                                   _prod_vectorized(self.M2, d2V))
        d2sdksi2 = _roll_vectorized(prod, 3*subtri, axis=0)
        return d2sdksi2
