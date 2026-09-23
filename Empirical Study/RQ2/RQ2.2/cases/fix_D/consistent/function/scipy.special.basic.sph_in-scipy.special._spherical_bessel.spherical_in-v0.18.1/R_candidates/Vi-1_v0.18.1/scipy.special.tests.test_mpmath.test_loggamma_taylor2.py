@check_version(mpmath, '0.19')
def test_loggamma_taylor2():
    # Test around the zeros at z = 1, 2.

    dx = np.r_[-np.logspace(-1, -16, 10), np.logspace(-16, -1, 10)]
    dy = dx.copy()
    dx, dy = np.meshgrid(dx, dy)
    dz = dx + 1j*dy
    z = np.r_[1 + dz, 2 + dz].flatten()
    dataset = []
    for z0 in z:
        dataset.append((z0, complex(mpmath.loggamma(z0))))

    dataset = np.array(dataset)
    FuncData(sc.loggamma, dataset, 0, 1, rtol=1e-13).check()
