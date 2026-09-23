@check_version(mpmath, '0.19')
def test_sinpi_zeros():
    eps = np.finfo(float).eps
    dx = np.r_[-np.logspace(0, -13, 3), 0, np.logspace(-13, 0, 3)]
    dy = dx.copy()
    dx, dy = np.meshgrid(dx, dy)
    dz = dx + 1j*dy
    zeros = np.arange(-100, 100, 1).reshape(1, 1, -1)
    z = (zeros + np.dstack((dz,)*zeros.size)).flatten()
    dataset = []
    for z0 in z:
        dataset.append((z0, complex(mpmath.sinpi(z0))))

    dataset = np.array(dataset)
    FuncData(_sinpi, dataset, 0, 1, rtol=2*eps).check()
