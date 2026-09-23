    def _eval_evalf(self, prec=15, **options):
        pt, tup = self.args
        dps = prec_to_dps(prec)
        pt = pt.evalf(n=dps, **options)
        tup = tuple([i.evalf(n=dps, **options) for i in tup])
        return self.func(pt, normal_vector=tup, evaluate=False)
