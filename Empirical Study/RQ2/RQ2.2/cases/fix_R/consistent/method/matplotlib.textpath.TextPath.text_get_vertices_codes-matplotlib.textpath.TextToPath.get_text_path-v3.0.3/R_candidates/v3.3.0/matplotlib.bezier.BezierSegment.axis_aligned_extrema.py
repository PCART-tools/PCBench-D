    def axis_aligned_extrema(self):
        """
        Return the dimension and location of the curve's interior extrema.

        The extrema are the points along the curve where one of its partial
        derivatives is zero.

        Returns
        -------
        dims : int, array_like
            Index :math:`i` of the partial derivative which is zero at each
            interior extrema.
        dzeros : float, array_like
            Of same size as dims. The :math:`t` such that :math:`d/dx_i B(t) =
            0`
        """
        n = self.degree
        Cj = self.polynomial_coefficients
        dCj = np.arange(1, n+1)[:, None] * Cj[1:]
        if len(dCj) == 0:
            return np.array([]), np.array([])
        dims = []
        roots = []
        for i, pi in enumerate(dCj.T):
            r = np.roots(pi[::-1])
            roots.append(r)
            dims.append(np.full_like(r, i))
        roots = np.concatenate(roots)
        dims = np.concatenate(dims)
        in_range = np.isreal(roots) & (roots >= 0) & (roots <= 1)
        return dims[in_range], np.real(roots)[in_range]
