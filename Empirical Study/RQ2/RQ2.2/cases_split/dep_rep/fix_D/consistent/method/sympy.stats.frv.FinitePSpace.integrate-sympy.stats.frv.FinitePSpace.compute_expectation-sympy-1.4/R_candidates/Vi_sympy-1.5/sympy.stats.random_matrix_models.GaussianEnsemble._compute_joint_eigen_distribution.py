    def _compute_joint_eigen_distribution(self, beta):
        """
        Helper function for computing the joint
        probability distribution of eigen values
        of the random matrix.
        """
        n = self.dimension
        Zbn = self._compute_normalization_constant(beta, n)
        l = IndexedBase('l')
        i = Dummy('i', integer=True, positive=True)
        j = Dummy('j', integer=True, positive=True)
        k = Dummy('k', integer=True, positive=True)
        term1 = exp((-S(n)/2) * Sum(l[k]**2, (k, 1, n)).doit())
        sub_term = Lambda(i, Product(Abs(l[j] - l[i])**beta, (j, i + 1, n)))
        term2 = Product(sub_term(i).doit(), (i, 1, n - 1)).doit()
        syms = ArrayComprehension(l[k], (k, 1, n)).doit()
        return Lambda(tuple(syms), (term1 * term2)/Zbn)
