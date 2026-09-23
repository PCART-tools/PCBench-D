    def transform_non_affine(self, a):
        """logistic transform (base 10)"""
        return 1.0 / (1 + 10**(-a))
