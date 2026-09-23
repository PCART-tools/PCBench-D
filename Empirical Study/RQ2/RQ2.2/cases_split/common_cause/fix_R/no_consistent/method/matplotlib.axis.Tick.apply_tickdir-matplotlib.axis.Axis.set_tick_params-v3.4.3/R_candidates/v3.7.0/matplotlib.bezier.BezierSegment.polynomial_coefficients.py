    @property
    def polynomial_coefficients(self):
        r"""
        The polynomial coefficients of the Bézier curve.

        .. warning:: Follows opposite convention from `numpy.polyval`.

        Returns
        -------
        (n+1, d) array
            Coefficients after expanding in polynomial basis, where :math:`n`
            is the degree of the Bézier curve and :math:`d` its dimension.
            These are the numbers (:math:`C_j`) such that the curve can be
            written :math:`\sum_{j=0}^n C_j t^j`.

        Notes
        -----
        The coefficients are calculated as

        .. math::

            {n \choose j} \sum_{i=0}^j (-1)^{i+j} {j \choose i} P_i

        where :math:`P_i` are the control points of the curve.
        """
        n = self.degree
        # matplotlib uses n <= 4. overflow plausible starting around n = 15.
        if n > 10:
            warnings.warn("Polynomial coefficients formula unstable for high "
                          "order Bezier curves!", RuntimeWarning)
        P = self.control_points
        j = np.arange(n+1)[:, None]
        i = np.arange(n+1)[None, :]  # _comb is non-zero for i <= j
        prefactor = (-1)**(i + j) * _comb(j, i)  # j on axis 0, i on axis 1
        return _comb(n, j) * prefactor @ P  # j on axis 0, self.dimension on 1
