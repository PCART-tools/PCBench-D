def test_hidden_axes():
    # test that if we make an axes not visible that constrained_layout
    # still works.  Note the axes still takes space in the layout
    # (as does a gridspec slot that is empty)
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    axs[0, 1].set_visible(False)
    fig.draw_without_rendering()
    extents1 = np.copy(axs[0, 0].get_position().extents)

    np.testing.assert_allclose(
        extents1, [0.045552, 0.543288, 0.47819, 0.982638], rtol=1e-5)
