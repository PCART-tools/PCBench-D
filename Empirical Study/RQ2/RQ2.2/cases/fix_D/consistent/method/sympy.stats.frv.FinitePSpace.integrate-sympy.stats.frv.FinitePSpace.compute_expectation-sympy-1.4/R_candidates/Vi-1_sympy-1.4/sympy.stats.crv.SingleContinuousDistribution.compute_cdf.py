    @cacheit
    def compute_cdf(self, **kwargs):
        """ Compute the CDF from the PDF

        Returns a Lambda
        """
        x, z = symbols('x, z', real=True, finite=True, cls=Dummy)
        left_bound = self.set.start

        # CDF is integral of PDF from left bound to z
        pdf = self.pdf(x)
        cdf = integrate(pdf, (x, left_bound, z), **kwargs)
        # CDF Ensure that CDF left of left_bound is zero
        cdf = Piecewise((cdf, z >= left_bound), (0, True))
        return Lambda(z, cdf)
