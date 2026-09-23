@dec.slow
@check_version(mpmath, '0.19')
def test_wrightomega_region1():
    # This region gets less coverage in the TestSystematic test
    x = np.linspace(-2, 1)
    y = np.linspace(1, 2*np.pi)
    x, y = np.meshgrid(x, y)
    z = (x + 1j*y).flatten()

    dataset = []
    for z0 in z:
        dataset.append((z0, complex(_mpmath_wrightomega(z0, 25))))
    dataset = np.asarray(dataset)

    FuncData(sc.wrightomega, dataset, 0, 1, rtol=1e-15).check()
