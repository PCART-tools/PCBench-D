def test_consistency():
    # Make sure the implementation of spence for real arguments
    # agrees with the implementation of spence for imaginary arguments.

    x = np.logspace(-30, 300, 200)
    dataset = np.vstack((x + 0j, spence(x))).T
    FuncData(spence, dataset, 0, 1, rtol=1e-14).check()
