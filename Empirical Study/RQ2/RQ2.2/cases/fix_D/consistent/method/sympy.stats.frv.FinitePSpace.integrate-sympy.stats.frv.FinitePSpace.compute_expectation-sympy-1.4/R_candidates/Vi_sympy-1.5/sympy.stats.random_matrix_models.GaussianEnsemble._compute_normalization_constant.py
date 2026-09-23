    def _compute_normalization_constant(self, beta, n):
        """
        Helper function for computing normalization
        constant for joint probability density of eigen
        values of Gaussian ensembles.

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Selberg_integral#Mehta's_integral
        """
        n = S(n)
        prod_term = lambda j: gamma(1 + beta*S(j)/2)/gamma(S.One + beta/S(2))
        j = Dummy('j', integer=True, positive=True)
        term1 = Product(prod_term(j), (j, 1, n)).doit()
        term2 = (2/(beta*n))**(beta*n*(n - 1)/4 + n/2)
        term3 = (2*pi)**(n/2)
        return term1 * term2 * term3
