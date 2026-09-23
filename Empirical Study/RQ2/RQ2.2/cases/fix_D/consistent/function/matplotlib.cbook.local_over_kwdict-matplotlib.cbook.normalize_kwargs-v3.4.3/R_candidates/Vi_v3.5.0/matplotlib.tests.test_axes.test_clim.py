def test_clim():
    ax = plt.figure().add_subplot()
    for plot_method in [ax.imshow, ax.pcolor, ax.pcolormesh, ax.pcolorfast]:
        clim = (7, 8)
        norm = plot_method([[0, 1], [2, 3]], clim=clim).norm
        assert (norm.vmin, norm.vmax) == clim
