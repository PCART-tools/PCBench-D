@image_comparison(['contour_colorbar'], style='mpl20')
def test_contour_colorbar():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    x, y, z = contour_dat()

    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, z, levels=np.arange(-1.8, 1.801, 0.2),
                     cmap=plt.get_cmap('RdBu'),
                     vmin=-0.6,
                     vmax=0.6,
                     extend='both')
    cs1 = ax.contour(x, y, z, levels=np.arange(-2.2, -0.599, 0.2),
                     colors=['y'],
                     linestyles='solid',
                     linewidths=2)
    cs2 = ax.contour(x, y, z, levels=np.arange(0.6, 2.2, 0.2),
                     colors=['c'],
                     linewidths=2)
    cbar = fig.colorbar(cs, ax=ax)
    cbar.add_lines(cs1)
    cbar.add_lines(cs2, erase=False)
