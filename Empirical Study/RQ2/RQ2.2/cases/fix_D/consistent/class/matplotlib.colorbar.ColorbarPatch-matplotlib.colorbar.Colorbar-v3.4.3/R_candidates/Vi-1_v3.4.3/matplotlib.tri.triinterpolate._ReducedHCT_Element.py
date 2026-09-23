class _ReducedHCT_Element:
    """
    Implementation of reduced HCT triangular element with explicit shape
    functions.

    Computes z, dz, d2z and the element stiffness matrix for bending energy:
    E(f) = integral( (d2z/dx2 + d2z/dy2)**2 dA)

    *** Reference for the shape functions: ***
    [1] Basis functions for general Hsieh-Clough-Tocher _triangles, complete or
        reduced.
        Michel Bernadou, Kamal Hassan
        International Journal for Numerical Methods in Engineering.
        17(5):784 - 789.  2.01

    *** Element description: ***
    9 dofs: z and dz given at 3 apex
    C1 (conform)

    """
    # 1) Loads matrices to generate shape functions as a function of
    #    triangle eccentricities - based on [1] p.11 '''
    M = np.array([
        [ 0.00, 0.00, 0.00,  4.50,  4.50, 0.00, 0.00, 0.00, 0.00, 0.00],
        [-0.25, 0.00, 0.00,  0.50,  1.25, 0.00, 0.00, 0.00, 0.00, 0.00],
        [-0.25, 0.00, 0.00,  1.25,  0.50, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.50, 1.00, 0.00, -1.50,  0.00, 3.00, 3.00, 0.00, 0.00, 3.00],
        [ 0.00, 0.00, 0.00, -0.25,  0.25, 0.00, 1.00, 0.00, 0.00, 0.50],
        [ 0.25, 0.00, 0.00, -0.50, -0.25, 1.00, 0.00, 0.00, 0.00, 1.00],
        [ 0.50, 0.00, 1.00,  0.00, -1.50, 0.00, 0.00, 3.00, 3.00, 3.00],
        [ 0.25, 0.00, 0.00, -0.25, -0.50, 0.00, 0.00, 0.00, 1.00, 1.00],
        [ 0.00, 0.00, 0.00,  0.25, -0.25, 0.00, 0.00, 1.00, 0.00, 0.50]])
    M0 = np.array([
        [ 0.00, 0.00, 0.00,  0.00,  0.00, 0.00, 0.00, 0.00, 0.00,  0.00],
        [ 0.00, 0.00, 0.00,  0.00,  0.00, 0.00, 0.00, 0.00, 0.00,  0.00],
        [ 0.00, 0.00, 0.00,  0.00,  0.00, 0.00, 0.00, 0.00, 0.00,  0.00],
        [-1.00, 0.00, 0.00,  1.50,  1.50, 0.00, 0.00, 0.00, 0.00, -3.00],
        [-0.50, 0.00, 0.00,  0.75,  0.75, 0.00, 0.00, 0.00, 0.00, -1.50],
        [ 0.00, 0.00, 0.00,  0.00,  0.00, 0.00, 0.00, 0.00, 0.00,  0.00],
        [ 1.00, 0.00, 0.00, -1.50, -1.50, 0.00, 0.00, 0.00, 0.00,  3.00],
        [ 0.00, 0.00, 0.00,  0.00,  0.00, 0.00, 0.00, 0.00, 0.00,  0.00],
        [ 0.50, 0.00, 0.00, -0.75, -0.75, 0.00, 0.00, 0.00, 0.00,  1.50]])
    M1 = np.array([
        [-0.50, 0.00, 0.00,  1.50, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [-0.25, 0.00, 0.00,  0.75, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.50, 0.00, 0.00, -1.50, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.25, 0.00, 0.00, -0.75, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])
    M2 = np.array([
        [ 0.50, 0.00, 0.00, 0.00, -1.50, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.25, 0.00, 0.00, 0.00, -0.75, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [-0.50, 0.00, 0.00, 0.00,  1.50, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [-0.25, 0.00, 0.00, 0.00,  0.75, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        [ 0.00, 0.00, 0.00, 0.00,  0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])

    # 2) Loads matrices to rotate components of gradient & Hessian
    #    vectors in the reference basis of triangle first apex (a0)
    rotate_dV = np.array([[ 1.,  0.], [ 0.,  1.],
                          [ 0.,  1.], [-1., -1.],
                          [-1., -1.], [ 1.,  0.]])

    rotate_d2V = np.array([[1., 0., 0.], [0., 1., 0.], [ 0.,  0.,  1.],
                           [0., 1., 0.], [1., 1., 1.], [ 0., -2., -1.],
                           [1., 1., 1.], [1., 0., 0.], [-2.,  0., -1.]])

    # 3) Loads Gauss points & weights on the 3 sub-_triangles for P2
    #    exact integral - 3 points on each subtriangles.
    # NOTE: as the 2nd derivative is discontinuous , we really need those 9
    # points!
    n_gauss = 9
    gauss_pts = np.array([[13./18.,  4./18.,  1./18.],
                          [ 4./18., 13./18.,  1./18.],
                          [ 7./18.,  7./18.,  4./18.],
                          [ 1./18., 13./18.,  4./18.],
                          [ 1./18.,  4./18., 13./18.],
                          [ 4./18.,  7./18.,  7./18.],
                          [ 4./18.,  1./18., 13./18.],
                          [13./18.,  1./18.,  4./18.],
                          [ 7./18.,  4./18.,  7./18.]], dtype=np.float64)
    gauss_w = np.ones([9], dtype=np.float64) / 9.

    #  4) Stiffness matrix for curvature energy
    E = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 2.]])

    #  5) Loads the matrix to compute DOF_rot from tri_J at apex 0
    J0_to_J1 = np.array([[-1.,  1.], [-1.,  0.]])
    J0_to_J2 = np.array([[ 0., -1.], [ 1., -1.]])

    def get_function_values(self, alpha, ecc, dofs):
        """
        Parameters
        ----------
        alpha : is a (N x 3 x 1) array (array of column-matrices) of
        barycentric coordinates,
        ecc : is a (N x 3 x 1) array (array of column-matrices) of triangle
        eccentricities,
        dofs : is a (N x 1 x 9) arrays (arrays of row-matrices) of computed
        degrees of freedom.

        Returns
        -------
        Returns the N-array of interpolated function values.
        """
        subtri = np.argmin(alpha, axis=1)[:, 0]
        ksi = _roll_vectorized(alpha, -subtri, axis=0)
        E = _roll_vectorized(ecc, -subtri, axis=0)
        x = ksi[:, 0, 0]
        y = ksi[:, 1, 0]
        z = ksi[:, 2, 0]
        x_sq = x*x
        y_sq = y*y
        z_sq = z*z
        V = _to_matrix_vectorized([
            [x_sq*x], [y_sq*y], [z_sq*z], [x_sq*z], [x_sq*y], [y_sq*x],
            [y_sq*z], [z_sq*y], [z_sq*x], [x*y*z]])
        prod = self.M @ V
        prod += _scalar_vectorized(E[:, 0, 0], self.M0 @ V)
        prod += _scalar_vectorized(E[:, 1, 0], self.M1 @ V)
        prod += _scalar_vectorized(E[:, 2, 0], self.M2 @ V)
        s = _roll_vectorized(prod, 3*subtri, axis=0)
        return (dofs @ s)[:, 0, 0]

    def get_function_derivatives(self, alpha, J, ecc, dofs):
        """
        Parameters
        ----------
        *alpha* is a (N x 3 x 1) array (array of column-matrices of
        barycentric coordinates)
        *J* is a (N x 2 x 2) array of jacobian matrices (jacobian matrix at
        triangle first apex)
        *ecc* is a (N x 3 x 1) array (array of column-matrices of triangle
        eccentricities)
        *dofs* is a (N x 1 x 9) arrays (arrays of row-matrices) of computed
        degrees of freedom.

        Returns
        -------
        Returns the values of interpolated function derivatives [dz/dx, dz/dy]
        in global coordinates at locations alpha, as a column-matrices of
        shape (N x 2 x 1).
        """
        subtri = np.argmin(alpha, axis=1)[:, 0]
        ksi = _roll_vectorized(alpha, -subtri, axis=0)
        E = _roll_vectorized(ecc, -subtri, axis=0)
        x = ksi[:, 0, 0]
        y = ksi[:, 1, 0]
        z = ksi[:, 2, 0]
        x_sq = x*x
        y_sq = y*y
        z_sq = z*z
        dV = _to_matrix_vectorized([
            [    -3.*x_sq,     -3.*x_sq],
            [     3.*y_sq,           0.],
            [          0.,      3.*z_sq],
            [     -2.*x*z, -2.*x*z+x_sq],
            [-2.*x*y+x_sq,      -2.*x*y],
            [ 2.*x*y-y_sq,        -y_sq],
            [      2.*y*z,         y_sq],
            [        z_sq,       2.*y*z],
            [       -z_sq,  2.*x*z-z_sq],
            [     x*z-y*z,      x*y-y*z]])
        # Puts back dV in first apex basis
        dV = dV @ _extract_submatrices(
            self.rotate_dV, subtri, block_size=2, axis=0)

        prod = self.M @ dV
        prod += _scalar_vectorized(E[:, 0, 0], self.M0 @ dV)
        prod += _scalar_vectorized(E[:, 1, 0], self.M1 @ dV)
        prod += _scalar_vectorized(E[:, 2, 0], self.M2 @ dV)
        dsdksi = _roll_vectorized(prod, 3*subtri, axis=0)
        dfdksi = dofs @ dsdksi
        # In global coordinates:
        # Here we try to deal with the simplest colinear cases, returning a
        # null matrix.
        J_inv = _safe_inv22_vectorized(J)
        dfdx = J_inv @ _transpose_vectorized(dfdksi)
        return dfdx

    def get_function_hessians(self, alpha, J, ecc, dofs):
        """
        Parameters
        ----------
        *alpha* is a (N x 3 x 1) array (array of column-matrices) of
        barycentric coordinates
        *J* is a (N x 2 x 2) array of jacobian matrices (jacobian matrix at
        triangle first apex)
        *ecc* is a (N x 3 x 1) array (array of column-matrices) of triangle
        eccentricities
        *dofs* is a (N x 1 x 9) arrays (arrays of row-matrices) of computed
        degrees of freedom.

        Returns
        -------
        Returns the values of interpolated function 2nd-derivatives
        [d2z/dx2, d2z/dy2, d2z/dxdy] in global coordinates at locations alpha,
        as a column-matrices of shape (N x 3 x 1).
        """
        d2sdksi2 = self.get_d2Sidksij2(alpha, ecc)
        d2fdksi2 = dofs @ d2sdksi2
        H_rot = self.get_Hrot_from_J(J)
        d2fdx2 = d2fdksi2 @ H_rot
        return _transpose_vectorized(d2fdx2)

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
        expressed in covariant coordinates in first apex basis.
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
        d2V = d2V @ _extract_submatrices(
            self.rotate_d2V, subtri, block_size=3, axis=0)
        prod = self.M @ d2V
        prod += _scalar_vectorized(E[:, 0, 0], self.M0 @ d2V)
        prod += _scalar_vectorized(E[:, 1, 0], self.M1 @ d2V)
        prod += _scalar_vectorized(E[:, 2, 0], self.M2 @ d2V)
        d2sdksi2 = _roll_vectorized(prod, 3*subtri, axis=0)
        return d2sdksi2

    def get_bending_matrices(self, J, ecc):
        """
        Parameters
        ----------
        *J* is a (N x 2 x 2) array of jacobian matrices (jacobian matrix at
        triangle first apex)
        *ecc* is a (N x 3 x 1) array (array of column-matrices) of triangle
        eccentricities

        Returns
        -------
        Returns the element K matrices for bending energy expressed in
        GLOBAL nodal coordinates.
        K_ij = integral [ (d2zi/dx2 + d2zi/dy2) * (d2zj/dx2 + d2zj/dy2) dA]
        tri_J is needed to rotate dofs from local basis to global basis
        """
        n = np.size(ecc, 0)

        # 1) matrix to rotate dofs in global coordinates
        J1 = self.J0_to_J1 @ J
        J2 = self.J0_to_J2 @ J
        DOF_rot = np.zeros([n, 9, 9], dtype=np.float64)
        DOF_rot[:, 0, 0] = 1
        DOF_rot[:, 3, 3] = 1
        DOF_rot[:, 6, 6] = 1
        DOF_rot[:, 1:3, 1:3] = J
        DOF_rot[:, 4:6, 4:6] = J1
        DOF_rot[:, 7:9, 7:9] = J2

        # 2) matrix to rotate Hessian in global coordinates.
        H_rot, area = self.get_Hrot_from_J(J, return_area=True)

        # 3) Computes stiffness matrix
        # Gauss quadrature.
        K = np.zeros([n, 9, 9], dtype=np.float64)
        weights = self.gauss_w
        pts = self.gauss_pts
        for igauss in range(self.n_gauss):
            alpha = np.tile(pts[igauss, :], n).reshape(n, 3)
            alpha = np.expand_dims(alpha, 2)
            weight = weights[igauss]
            d2Skdksi2 = self.get_d2Sidksij2(alpha, ecc)
            d2Skdx2 = d2Skdksi2 @ H_rot
            K += weight * (d2Skdx2 @ self.E @ _transpose_vectorized(d2Skdx2))

        # 4) With nodal (not elem) dofs
        K = _transpose_vectorized(DOF_rot) @ K @ DOF_rot

        # 5) Need the area to compute total element energy
        return _scalar_vectorized(area, K)

    def get_Hrot_from_J(self, J, return_area=False):
        """
        Parameters
        ----------
        *J* is a (N x 2 x 2) array of jacobian matrices (jacobian matrix at
        triangle first apex)

        Returns
        -------
        Returns H_rot used to rotate Hessian from local basis of first apex,
        to global coordinates.
        if *return_area* is True, returns also the triangle area (0.5*det(J))
        """
        # Here we try to deal with the simplest colinear cases; a null
        # energy and area is imposed.
        J_inv = _safe_inv22_vectorized(J)
        Ji00 = J_inv[:, 0, 0]
        Ji11 = J_inv[:, 1, 1]
        Ji10 = J_inv[:, 1, 0]
        Ji01 = J_inv[:, 0, 1]
        H_rot = _to_matrix_vectorized([
            [Ji00*Ji00, Ji10*Ji10, Ji00*Ji10],
            [Ji01*Ji01, Ji11*Ji11, Ji01*Ji11],
            [2*Ji00*Ji01, 2*Ji11*Ji10, Ji00*Ji11+Ji10*Ji01]])
        if not return_area:
            return H_rot
        else:
            area = 0.5 * (J[:, 0, 0]*J[:, 1, 1] - J[:, 0, 1]*J[:, 1, 0])
            return H_rot, area

    def get_Kff_and_Ff(self, J, ecc, triangles, Uc):
        """
        Build K and F for the following elliptic formulation:
        minimization of curvature energy with value of function at node
        imposed and derivatives 'free'.

        Build the global Kff matrix in cco format.
        Build the full Ff vec Ff = - Kfc x Uc.

        Parameters
        ----------
        *J* is a (N x 2 x 2) array of jacobian matrices (jacobian matrix at
        triangle first apex)
        *ecc* is a (N x 3 x 1) array (array of column-matrices) of triangle
        eccentricities
        *triangles* is a (N x 3) array of nodes indexes.
        *Uc* is (N x 3) array of imposed displacements at nodes

        Returns
        -------
        (Kff_rows, Kff_cols, Kff_vals) Kff matrix in coo format - Duplicate
        (row, col) entries must be summed.
        Ff: force vector - dim npts * 3
        """
        ntri = np.size(ecc, 0)
        vec_range = np.arange(ntri, dtype=np.int32)
        c_indices = np.full(ntri, -1, dtype=np.int32)  # for unused dofs, -1
        f_dof = [1, 2, 4, 5, 7, 8]
        c_dof = [0, 3, 6]

        # vals, rows and cols indices in global dof numbering
        f_dof_indices = _to_matrix_vectorized([[
            c_indices, triangles[:, 0]*2, triangles[:, 0]*2+1,
            c_indices, triangles[:, 1]*2, triangles[:, 1]*2+1,
            c_indices, triangles[:, 2]*2, triangles[:, 2]*2+1]])

        expand_indices = np.ones([ntri, 9, 1], dtype=np.int32)
        f_row_indices = _transpose_vectorized(expand_indices @ f_dof_indices)
        f_col_indices = expand_indices @ f_dof_indices
        K_elem = self.get_bending_matrices(J, ecc)

        # Extracting sub-matrices
        # Explanation & notations:
        # * Subscript f denotes 'free' degrees of freedom (i.e. dz/dx, dz/dx)
        # * Subscript c denotes 'condensated' (imposed) degrees of freedom
        #    (i.e. z at all nodes)
        # * F = [Ff, Fc] is the force vector
        # * U = [Uf, Uc] is the imposed dof vector
        #        [ Kff Kfc ]
        # * K =  [         ]  is the laplacian stiffness matrix
        #        [ Kcf Kff ]
        # * As F = K x U one gets straightforwardly: Ff = - Kfc x Uc

        # Computing Kff stiffness matrix in sparse coo format
        Kff_vals = np.ravel(K_elem[np.ix_(vec_range, f_dof, f_dof)])
        Kff_rows = np.ravel(f_row_indices[np.ix_(vec_range, f_dof, f_dof)])
        Kff_cols = np.ravel(f_col_indices[np.ix_(vec_range, f_dof, f_dof)])

        # Computing Ff force vector in sparse coo format
        Kfc_elem = K_elem[np.ix_(vec_range, f_dof, c_dof)]
        Uc_elem = np.expand_dims(Uc, axis=2)
        Ff_elem = -(Kfc_elem @ Uc_elem)[:, :, 0]
        Ff_indices = f_dof_indices[np.ix_(vec_range, [0], f_dof)][:, 0, :]

        # Extracting Ff force vector in dense format
        # We have to sum duplicate indices -  using bincount
        Ff = np.bincount(np.ravel(Ff_indices), weights=np.ravel(Ff_elem))
        return Kff_rows, Kff_cols, Kff_vals, Ff
