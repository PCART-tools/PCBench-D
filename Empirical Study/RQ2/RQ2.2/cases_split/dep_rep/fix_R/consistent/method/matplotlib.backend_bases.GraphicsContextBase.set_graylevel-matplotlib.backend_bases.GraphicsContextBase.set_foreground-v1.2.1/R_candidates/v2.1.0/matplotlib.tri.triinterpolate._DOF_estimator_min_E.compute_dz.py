    def compute_dz(self):
        """
        Elliptic solver for bending energy minimization.
        Uses a dedicated 'toy' sparse Jacobi PCG solver.
        """
        # Initial guess for iterative PCG solver.
        dz_init = _DOF_estimator_geom.compute_dz(self)
        Uf0 = np.ravel(dz_init)

        reference_element = _ReducedHCT_Element()
        J = CubicTriInterpolator._get_jacobian(self._tris_pts)
        eccs = self._eccs
        triangles = self._triangles
        Uc = self.z[self._triangles]

        # Building stiffness matrix and force vector in coo format
        Kff_rows, Kff_cols, Kff_vals, Ff = reference_element.get_Kff_and_Ff(
            J, eccs, triangles, Uc)

        # Building sparse matrix and solving minimization problem
        # We could use scipy.sparse direct solver ; however to avoid this
        # external dependency an implementation of a simple PCG solver with
        # a simplendiagonal Jocabi preconditioner is implemented.
        tol = 1.e-10
        n_dof = Ff.shape[0]
        Kff_coo = _Sparse_Matrix_coo(Kff_vals, Kff_rows, Kff_cols,
                                     shape=(n_dof, n_dof))
        Kff_coo.compress_csc()
        Uf, err = _cg(A=Kff_coo, b=Ff, x0=Uf0, tol=tol)
        # If the PCG did not converge, we return the best guess between Uf0
        # and Uf.
        err0 = np.linalg.norm(Kff_coo.dot(Uf0) - Ff)
        if err0 < err:
            # Maybe a good occasion to raise a warning here ?
            warnings.warn("In TriCubicInterpolator initialization, PCG sparse"
                          " solver did not converge after 1000 iterations. "
                          "`geom` approximation is used instead of `min_E`")
            Uf = Uf0

        # Building dz from Uf
        dz = np.empty([self._pts.shape[0], 2], dtype=np.float64)
        dz[:, 0] = Uf[::2]
        dz[:, 1] = Uf[1::2]
        return dz
