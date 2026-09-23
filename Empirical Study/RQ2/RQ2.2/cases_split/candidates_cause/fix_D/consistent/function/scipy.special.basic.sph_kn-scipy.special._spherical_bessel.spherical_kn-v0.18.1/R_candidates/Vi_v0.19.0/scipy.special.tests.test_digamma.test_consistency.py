def test_consistency():
    # Make sure the implementation of digamma for real arguments
    # agrees with the implementation of digamma for complex arguments.

    # It's all poles after -1e16
    x = np.r_[-np.logspace(15, -30, 200), np.logspace(-30, 300, 200)]
    dataset = np.vstack((x + 0j, digamma(x))).T
    FuncData(digamma, dataset, 0, 1, rtol=5e-14, nan_ok=True).check()
