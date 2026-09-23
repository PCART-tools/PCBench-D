    def _moment_generating_function(self, t):
        k = self.k

        part_1 = hyper((k / 2,), (S.Half,), t ** 2 / 2)
        part_2 = t * sqrt(2) * gamma((k + 1) / 2) / gamma(k / 2)
        part_3 = hyper(((k + 1) / 2,), (S(3) / 2,), t ** 2 / 2)
        return part_1 + part_2 * part_3
