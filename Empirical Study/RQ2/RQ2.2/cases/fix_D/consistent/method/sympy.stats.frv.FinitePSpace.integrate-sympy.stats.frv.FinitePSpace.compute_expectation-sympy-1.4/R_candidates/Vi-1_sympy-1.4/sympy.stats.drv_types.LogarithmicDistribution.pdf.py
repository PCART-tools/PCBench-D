    def pdf(self, k):
        p = self.p
        return (-1) * p**k / (k * log(1 - p))
