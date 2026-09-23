@check_version(mpmath, '0.19')
def test_loggamma_taylor1():
    # Make sure there isn't a big jump in accuracy when we move from
    # using the Taylor series to using the recurrence relation.

    pts = [-0.5, 0.5j, -0.5j, 0.5, 1 + 0.5j, 1 - 0.5j, 1.5, 2 - 0.5j,
           2 + 0.5j, 2.5]
    dataset = []
    for p in pts:
        for eps in [1e-6, -1e-6, 1e-6j, -1e-6j]:
            q = p + eps
            dataset.append((q, complex(mpmath.loggamma(q))))
        
    dataset = np.array(dataset)
    FuncData(sc.loggamma, dataset, 0, 1, rtol=1e-13).check()
