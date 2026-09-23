def test_contour_badlevel_fmt():
    # Test edge case from https://github.com/matplotlib/matplotlib/issues/9742
    # User supplied fmt for each level as a dictionary, but Matplotlib changed
    # the level to the minimum data value because no contours possible.
    # This was fixed in https://github.com/matplotlib/matplotlib/pull/9743
    x = np.arange(9)
    z = np.zeros((9, 9))

    fig, ax = plt.subplots()
    fmt = {1.: '%1.2f'}
    with pytest.warns(UserWarning) as record:
        cs = ax.contour(x, x, z, levels=[1.])
        ax.clabel(cs, fmt=fmt)
    assert len(record) == 1
