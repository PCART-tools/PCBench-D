@image_comparison(['levels_and_colors.png'])
def test_cmap_and_norm_from_levels_and_colors():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    data = np.linspace(-2, 4, 49).reshape(7, 7)
    levels = [-1, 2, 2.5, 3]
    colors = ['red', 'green', 'blue', 'yellow', 'black']
    extend = 'both'
    cmap, norm = mcolors.from_levels_and_colors(levels, colors, extend=extend)

    ax = plt.axes()
    m = plt.pcolormesh(data, cmap=cmap, norm=norm)
    plt.colorbar(m)

    # Hide the axes labels (but not the colorbar ones, as they are useful)
    ax.tick_params(labelleft=False, labelbottom=False)
