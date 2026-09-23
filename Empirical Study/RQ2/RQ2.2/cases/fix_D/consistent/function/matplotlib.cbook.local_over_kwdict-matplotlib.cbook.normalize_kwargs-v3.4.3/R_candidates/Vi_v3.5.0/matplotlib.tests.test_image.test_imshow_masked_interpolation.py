@image_comparison(['imshow_masked_interpolation'],
                  tol=0 if platform.machine() == 'x86_64' else 0.01,
                  remove_text=True, style='mpl20')
def test_imshow_masked_interpolation():

    cmap = plt.get_cmap('viridis').with_extremes(over='r', under='b', bad='k')

    N = 20
    n = colors.Normalize(vmin=0, vmax=N*N-1)

    data = np.arange(N*N, dtype=float).reshape(N, N)

    data[5, 5] = -1
    # This will cause crazy ringing for the higher-order
    # interpolations
    data[15, 5] = 1e5

    # data[3, 3] = np.nan

    data[15, 15] = np.inf

    mask = np.zeros_like(data).astype('bool')
    mask[5, 15] = True

    data = np.ma.masked_array(data, mask)

    fig, ax_grid = plt.subplots(3, 6)
    interps = sorted(mimage._interpd_)
    interps.remove('antialiased')

    for interp, ax in zip(interps, ax_grid.ravel()):
        ax.set_title(interp)
        ax.imshow(data, norm=n, cmap=cmap, interpolation=interp)
        ax.axis('off')
