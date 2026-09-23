    @cacheit
    def compute_quantile(self, **kwargs):
        """ Compute the Quantile from the PDF

        Returns a Lambda
        """
        x = Dummy('x', integer=True)
        p = Dummy('p', real=True)
        left_bound = self.set.inf
        pdf = self.pdf(x)
        cdf = summation(pdf, (x, left_bound, x), **kwargs)
        set = ((x, p <= cdf), )
        return Lambda(p, Piecewise(*set))
