    @cacheit
    def compute_quantile(self, **kwargs):
        """ Compute the Quantile from the PDF

        Returns a Lambda
        """
        x, p = symbols('x, p', real=True, cls=Dummy)
        left_bound = self.set.start

        pdf = self.pdf(x)
        cdf = integrate(pdf, (x, left_bound, x), **kwargs)

        quantile = solveset(cdf - p, x, S.Reals)
        return Lambda(p, Piecewise((quantile, (p >= 0) & (p <= 1) ), (nan, True)))
