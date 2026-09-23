def test_colorbar_lognorm_extension():
    # Test that colorbar with lognorm is extended correctly
    f, ax = plt.subplots()
    cb = ColorbarBase(ax, norm=LogNorm(vmin=0.1, vmax=1000.0),
                      orientation='vertical', extend='both')
    assert cb._values[0] >= 0.0
