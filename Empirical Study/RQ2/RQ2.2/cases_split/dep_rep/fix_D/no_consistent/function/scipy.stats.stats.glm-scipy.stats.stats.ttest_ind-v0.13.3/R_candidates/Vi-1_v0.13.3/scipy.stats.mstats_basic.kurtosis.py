def kurtosis(a, axis=0, fisher=True, bias=True):
    a, axis = _chk_asarray(a, axis)
    m2 = moment(a,2,axis)
    m4 = moment(a,4,axis)
    olderr = np.seterr(all='ignore')
    try:
        vals = ma.where(m2 == 0, 0, m4 / m2**2.0)
    finally:
        np.seterr(**olderr)

    if not bias:
        n = a.count(axis)
        can_correct = (n > 3) & (m2 is not ma.masked and m2 > 0)
        if can_correct.any():
            n = np.extract(can_correct, n)
            m2 = np.extract(can_correct, m2)
            m4 = np.extract(can_correct, m4)
            nval = 1.0/(n-2)/(n-3)*((n*n-1.0)*m4/m2**2.0-3*(n-1)**2.0)
            np.place(vals, can_correct, nval+3.0)
    if fisher:
        return vals - 3
    else:
        return vals
