@check_version(mpmath, '0.19')
@dec.slow
def test_gammainc_boundary():
    # Test the transition to the asymptotic series.
    small = 25
    a = np.linspace(0.5*0.7*small, 2*1.3*small, 100)
    x = a.copy()
    a, x = np.meshgrid(a, x)
    a, x = a.flatten(), x.flatten()
    dataset = []
    with mpmath.workdps(100):
        for a0, x0 in zip(a, x):
            dataset.append((a0, x0, float(mpmath.gammainc(a0, b=x0, regularized=True))))
    dataset = np.array(dataset)

    FuncData(sc.gammainc, dataset, (0, 1), 2, rtol=1e-12).check()
