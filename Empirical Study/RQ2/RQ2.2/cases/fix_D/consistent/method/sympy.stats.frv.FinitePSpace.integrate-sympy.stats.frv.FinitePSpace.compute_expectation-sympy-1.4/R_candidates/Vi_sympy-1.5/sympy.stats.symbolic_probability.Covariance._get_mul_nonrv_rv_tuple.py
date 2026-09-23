    @classmethod
    def _get_mul_nonrv_rv_tuple(cls, m):
        rv = []
        nonrv = []
        for a in m.args:
            if a.has(RandomSymbol):
                rv.append(a)
            else:
                nonrv.append(a)
        return (Mul(*nonrv), Mul(*rv))
