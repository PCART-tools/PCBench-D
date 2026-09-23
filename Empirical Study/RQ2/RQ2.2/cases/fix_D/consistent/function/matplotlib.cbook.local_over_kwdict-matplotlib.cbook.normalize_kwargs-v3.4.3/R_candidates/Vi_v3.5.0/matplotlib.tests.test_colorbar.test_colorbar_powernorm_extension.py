def test_colorbar_powernorm_extension():
    # Test that colorbar with powernorm is extended correctly
    f, ax = plt.subplots()
    cb = Colorbar(ax, norm=PowerNorm(gamma=0.5, vmin=0.0, vmax=1.0),
                  orientation='vertical', extend='both')
    assert cb._values[0] >= 0.0
