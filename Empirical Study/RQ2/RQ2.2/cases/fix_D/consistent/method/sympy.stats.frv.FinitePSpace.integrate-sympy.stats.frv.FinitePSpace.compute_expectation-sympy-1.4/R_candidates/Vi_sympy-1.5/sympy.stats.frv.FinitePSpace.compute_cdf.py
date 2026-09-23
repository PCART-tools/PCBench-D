    @cacheit
    def compute_cdf(self, expr):
        d = self.compute_density(expr)
        cum_prob = S.Zero
        cdf = []
        for key in sorted(d):
            prob = d[key]
            cum_prob += prob
            cdf.append((key, cum_prob))

        return dict(cdf)
