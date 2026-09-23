    def _compute_joint_eigen_distribution(self, beta):
        """
        Helper function to compute the joint distribution of phases
        of the complex eigen values of matrices belonging to any
        circular ensembles.
        """
        n = self.dimension
        Zbn = ((2*pi)**n)*(gamma(beta*n/2 + 1)/S((gamma(beta/2 + 1)))**n)
        t = IndexedBase('t')
        i, j, k = (Dummy('i', integer=True), Dummy('j', integer=True),
                   Dummy('k', integer=True))
        syms = ArrayComprehension(t[i], (i, 1, n)).doit()
        f = Product(Product(Abs(exp(I*t[k]) - exp(I*t[j]))**beta, (j, k + 1, n)).doit(),
                    (k, 1, n - 1)).doit()
        return Lambda(tuple(syms), f/Zbn)
