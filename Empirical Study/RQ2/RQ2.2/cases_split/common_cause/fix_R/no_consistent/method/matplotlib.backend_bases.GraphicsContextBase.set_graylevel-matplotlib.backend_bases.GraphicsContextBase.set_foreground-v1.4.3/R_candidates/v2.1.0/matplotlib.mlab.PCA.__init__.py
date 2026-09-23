    def __init__(self, a, standardize=True):
        """
        compute the SVD of a and store data for PCA.  Use project to
        project the data onto a reduced set of dimensions

        Parameters
        ----------
        a : np.ndarray
            A numobservations x numdims array
        standardize : bool
            True if input data are to be standardized. If False, only centering
            will be carried out.

        Attributes
        ----------
        a
            A centered unit sigma version of input ``a``.

        numrows, numcols
            The dimensions of ``a``.

        mu
            A numdims array of means of ``a``. This is the vector that points
            to the origin of PCA space.

        sigma
            A numdims array of standard deviation of ``a``.

        fracs
            The proportion of variance of each of the principal components.

        s
            The actual eigenvalues of the decomposition.

        Wt
            The weight vector for projecting a numdims point or array into
            PCA space.

        Y
            A projected into PCA space.

        Notes
        -----
        The factor loadings are in the ``Wt`` factor, i.e., the factor loadings
        for the first principal component are given by ``Wt[0]``. This row is
        also the first eigenvector.

        """
        n, m = a.shape
        if n < m:
            raise RuntimeError('we assume data in a is organized with '
                               'numrows>numcols')

        self.numrows, self.numcols = n, m
        self.mu = a.mean(axis=0)
        self.sigma = a.std(axis=0)
        self.standardize = standardize

        a = self.center(a)

        self.a = a

        U, s, Vh = np.linalg.svd(a, full_matrices=False)

        # Note: .H indicates the conjugate transposed / Hermitian.

        # The SVD is commonly written as a = U s V.H.
        # If U is a unitary matrix, it means that it satisfies U.H = inv(U).

        # The rows of Vh are the eigenvectors of a.H a.
        # The columns of U are the eigenvectors of a a.H.
        # For row i in Vh and column i in U, the corresponding eigenvalue is
        # s[i]**2.

        self.Wt = Vh

        # save the transposed coordinates
        Y = np.dot(Vh, a.T).T
        self.Y = Y

        # save the eigenvalues
        self.s = s**2

        # and now the contribution of the individual components
        vars = self.s/float(len(s))
        self.fracs = vars/vars.sum()
