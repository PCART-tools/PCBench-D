    def _eval_evalf(self, prec=15, **options):
        pt, r = self.args
        dps = prec_to_dps(prec)
        pt = pt.evalf(n=dps, **options)
        r = r.evalf(n=dps, **options)
        return self.func(pt, r, evaluate=False)
