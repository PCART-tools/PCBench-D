def test_gca():
    fig = plt.figure()

    with pytest.warns(UserWarning):
        # empty call to add_axes() will throw deprecation warning
        assert fig.add_axes() is None

    ax0 = fig.add_axes([0, 0, 1, 1])
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        assert fig.gca(projection='rectilinear') is ax0
    assert fig.gca() is ax0

    ax1 = fig.add_axes(rect=[0.1, 0.1, 0.8, 0.8])
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        assert fig.gca(projection='rectilinear') is ax1
    assert fig.gca() is ax1

    ax2 = fig.add_subplot(121, projection='polar')
    assert fig.gca() is ax2
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        assert fig.gca(polar=True) is ax2

    ax3 = fig.add_subplot(122)
    assert fig.gca() is ax3

    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        assert fig.gca(polar=True) is ax3
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        assert fig.gca(polar=True) is not ax2
    assert fig.gca().get_subplotspec().get_geometry() == (1, 2, 1, 1)

    # add_axes on an existing Axes should not change stored order, but will
    # make it current.
    fig.add_axes(ax0)
    assert fig.axes == [ax0, ax1, ax2, ax3]
    assert fig.gca() is ax0

    # add_subplot on an existing Axes should not change stored order, but will
    # make it current.
    fig.add_subplot(ax2)
    assert fig.axes == [ax0, ax1, ax2, ax3]
    assert fig.gca() is ax2

    fig.sca(ax1)
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        assert fig.gca(projection='rectilinear') is ax1
    assert fig.gca() is ax1

    # sca() should not change stored order of Axes, which is order added.
    assert fig.axes == [ax0, ax1, ax2, ax3]
