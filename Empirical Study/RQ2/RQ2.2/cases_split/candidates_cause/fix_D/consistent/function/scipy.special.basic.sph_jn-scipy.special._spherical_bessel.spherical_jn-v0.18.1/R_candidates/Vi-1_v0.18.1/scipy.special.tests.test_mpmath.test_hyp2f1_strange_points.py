@check_version(mpmath, '0.14')
def test_hyp2f1_strange_points():
    pts = [
        (2, -1, -1, 0.7),
        (2, -2, -2, 0.7),
    ]
    kw = dict(eliminate=True)
    dataset = [p + (float(mpmath.hyp2f1(*p, **kw)),) for p in pts]
    dataset = np.array(dataset, dtype=np.float_)

    FuncData(sc.hyp2f1, dataset, (0,1,2,3), 4, rtol=1e-10).check()
