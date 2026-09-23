    def pdf(self, k):
        return self.lamda**k / factorial(k) * exp(-self.lamda)
