def test_as_mpl_axes_api():
    # tests the _as_mpl_axes api
    from matplotlib.projections.polar import PolarAxes

    class Polar:
        def __init__(self):
            self.theta_offset = 0

        def _as_mpl_axes(self):
            # implement the matplotlib axes interface
            return PolarAxes, {'theta_offset': self.theta_offset}

    prj = Polar()
    prj2 = Polar()
    prj2.theta_offset = np.pi
    prj3 = Polar()

    # testing axes creation with plt.axes
    ax = plt.axes([0, 0, 1, 1], projection=prj)
    assert type(ax) == PolarAxes
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax_via_gca = plt.gca(projection=prj)
    assert ax_via_gca is ax
    plt.close()

    # testing axes creation with gca
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax = plt.gca(projection=prj)
    assert type(ax) == mpl.axes._subplots.subplot_class_factory(PolarAxes)
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax_via_gca = plt.gca(projection=prj)
    assert ax_via_gca is ax
    # try getting the axes given a different polar projection
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax_via_gca = plt.gca(projection=prj2)
    assert ax_via_gca is ax
    assert ax.get_theta_offset() == 0
    # try getting the axes given an == (not is) polar projection
    with pytest.warns(
            MatplotlibDeprecationWarning,
            match=r'Calling gca\(\) with keyword arguments was deprecated'):
        ax_via_gca = plt.gca(projection=prj3)
    assert ax_via_gca is ax
    plt.close()

    # testing axes creation with subplot
    ax = plt.subplot(121, projection=prj)
    assert type(ax) == mpl.axes._subplots.subplot_class_factory(PolarAxes)
    plt.close()
