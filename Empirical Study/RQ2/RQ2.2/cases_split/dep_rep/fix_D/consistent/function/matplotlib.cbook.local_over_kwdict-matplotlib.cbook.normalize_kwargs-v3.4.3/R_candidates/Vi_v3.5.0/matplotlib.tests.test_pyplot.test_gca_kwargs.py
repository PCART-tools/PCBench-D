def test_gca_kwargs():
    # plt.gca() returns an existing axes, unless there were no axes.
    plt.figure()
    ax = plt.gca()
    ax1 = plt.gca()
    assert ax is not None
    assert ax1 is ax
    plt.close()

    # plt.gca() raises a DeprecationWarning if called with kwargs.
    plt.figure()
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax = plt.gca(projection='polar')
    ax1 = plt.gca()
    assert ax is not None
    assert ax1 is ax
    assert ax1.name == 'polar'
    plt.close()

    # plt.gca() ignores keyword arguments if an axes already exists.
    plt.figure()
    ax = plt.gca()
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax1 = plt.gca(projection='polar')
    assert ax is not None
    assert ax1 is ax
    assert ax1.name == 'rectilinear'
    plt.close()
