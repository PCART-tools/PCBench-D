def test_tick_apply_tickdir_deprecation():
    # Remove this test when the deprecation expires.
    import matplotlib.axis as maxis
    ax = plt.axes()

    tick = maxis.XTick(ax, 0)
    with pytest.warns(MatplotlibDeprecationWarning,
                      match="The apply_tickdir function was deprecated in "
                            "Matplotlib 3.5"):
        tick.apply_tickdir('out')

    tick = maxis.YTick(ax, 0)
    with pytest.warns(MatplotlibDeprecationWarning,
                      match="The apply_tickdir function was deprecated in "
                            "Matplotlib 3.5"):
        tick.apply_tickdir('out')
