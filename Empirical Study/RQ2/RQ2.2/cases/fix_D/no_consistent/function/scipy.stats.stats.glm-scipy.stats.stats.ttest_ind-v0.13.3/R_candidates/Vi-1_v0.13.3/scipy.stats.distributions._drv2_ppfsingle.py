def _drv2_ppfsingle(self, q, *args):  # Use basic bisection algorithm
    b = self.b
    a = self.a
    if isinf(b):            # Be sure ending point is > q
        b = int(max(100*q,10))
        while 1:
            if b >= self.b:
                qb = 1.0
                break
            qb = self._cdf(b,*args)
            if (qb < q):
                b += 10
            else:
                break
    else:
        qb = 1.0
    if isinf(a):    # be sure starting point < q
        a = int(min(-100*q,-10))
        while 1:
            if a <= self.a:
                qb = 0.0
                break
            qa = self._cdf(a,*args)
            if (qa > q):
                a -= 10
            else:
                break
    else:
        qa = self._cdf(a, *args)

    while 1:
        if (qa == q):
            return a
        if (qb == q):
            return b
        if b <= a+1:
    # testcase: return wrong number at lower index
    # python -c "from scipy.stats import zipf;print zipf.ppf(0.01,2)" wrong
    # python -c "from scipy.stats import zipf;print zipf.ppf([0.01,0.61,0.77,0.83],2)"
    # python -c "from scipy.stats import logser;print logser.ppf([0.1,0.66, 0.86,0.93],0.6)"
            if qa > q:
                return a
            else:
                return b
        c = int((a+b)/2.0)
        qc = self._cdf(c, *args)
        if (qc < q):
            if a != c:
                a = c
            else:
                raise RuntimeError('updating stopped, endless loop')
            qa = qc
        elif (qc > q):
            if b != c:
                b = c
            else:
                raise RuntimeError('updating stopped, endless loop')
            qb = qc
        else:
            return c
