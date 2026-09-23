def test_constrained_layout21():
    """#11035: repeated calls to suptitle should not alter the layout"""
    fig, ax = plt.subplots(constrained_layout=True)

    fig.suptitle("Suptitle0")
    fig.canvas.draw()
    extents0 = np.copy(ax.get_position().extents)

    fig.suptitle("Suptitle1")
    fig.canvas.draw()
    extents1 = np.copy(ax.get_position().extents)

    np.testing.assert_allclose(extents0, extents1)
