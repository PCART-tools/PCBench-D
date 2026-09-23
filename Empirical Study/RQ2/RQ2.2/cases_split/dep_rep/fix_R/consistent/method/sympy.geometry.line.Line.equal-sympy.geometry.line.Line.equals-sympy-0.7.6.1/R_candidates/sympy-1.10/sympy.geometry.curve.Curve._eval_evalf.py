    def _eval_evalf(self, prec=15, **options):
        f, (t, a, b) = self.args
        dps = prec_to_dps(prec)
        f = tuple([i.evalf(n=dps, **options) for i in f])
        a, b = [i.evalf(n=dps, **options) for i in (a, b)]
        return self.func(f, (t, a, b))
