@pytest.mark.parametrize('extend, levels', [['both', [2, 4, 6]],
                                            ['min', [2, 4, 6, 8]],
                                            ['max', [0, 2, 4, 6]]])
@check_figures_equal(extensions=["png"])
def test_contourf3d_extend(fig_test, fig_ref, extend, levels):
    X, Y = np.meshgrid(np.arange(-2, 2, 0.25), np.arange(-2, 2, 0.25))
    # Z is in the range [0, 8]
    Z = X**2 + Y**2

    # Manually set the over/under colors to be the end of the colormap
    cmap = mpl.colormaps['viridis'].copy()
    cmap.set_under(cmap(0))
    cmap.set_over(cmap(255))
    # Set vmin/max to be the min/max values plotted on the reference image
    kwargs = {'vmin': 1, 'vmax': 7, 'cmap': cmap}

    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.contourf(X, Y, Z, levels=[0, 2, 4, 6, 8], **kwargs)

    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.contourf(X, Y, Z, levels, extend=extend, **kwargs)

    for ax in [ax_ref, ax_test]:
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-10, 10)
