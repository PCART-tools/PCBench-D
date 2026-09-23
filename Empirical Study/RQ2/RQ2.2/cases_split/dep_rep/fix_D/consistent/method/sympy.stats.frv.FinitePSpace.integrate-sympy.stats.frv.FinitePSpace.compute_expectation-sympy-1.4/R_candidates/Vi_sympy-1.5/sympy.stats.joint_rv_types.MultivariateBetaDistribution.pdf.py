    def pdf(self, *syms):
        alpha = self.alpha
        B = Mul.fromiter(map(gamma, alpha))/gamma(Add(*alpha))
        return Mul.fromiter([sym**(a_k - 1) for a_k, sym in zip(alpha, syms)])/B
