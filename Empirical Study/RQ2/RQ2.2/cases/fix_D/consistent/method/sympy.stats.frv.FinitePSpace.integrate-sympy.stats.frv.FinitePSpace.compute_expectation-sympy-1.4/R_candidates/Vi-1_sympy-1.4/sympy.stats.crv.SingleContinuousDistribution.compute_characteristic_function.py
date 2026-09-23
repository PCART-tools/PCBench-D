    @cacheit
    def compute_characteristic_function(self, **kwargs):
        """ Compute the characteristic function from the PDF

        Returns a Lambda
        """
        x, t = symbols('x, t', real=True, finite=True, cls=Dummy)
        pdf = self.pdf(x)
        cf = integrate(exp(I*t*x)*pdf, (x, -oo, oo))
        return Lambda(t, cf)
