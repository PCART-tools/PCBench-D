    @check_figures_equal(extensions=["png"])
    @pytest.mark.parametrize(
        "x", [[["A", "A", "B"], ["C", "D", "B"]], [[1, 1, 2], [3, 4, 2]]]
    )
    def test_basic(self, fig_test, fig_ref, x):
        grid_axes = fig_test.subplot_mosaic(x)

        for k, ax in grid_axes.items():
            ax.set_title(k)

        labels = sorted(np.unique(x))

        assert len(labels) == len(grid_axes)

        gs = fig_ref.add_gridspec(2, 3)
        axA = fig_ref.add_subplot(gs[:1, :2])
        axA.set_title(labels[0])

        axB = fig_ref.add_subplot(gs[:, 2])
        axB.set_title(labels[1])

        axC = fig_ref.add_subplot(gs[1, 0])
        axC.set_title(labels[2])

        axD = fig_ref.add_subplot(gs[1, 1])
        axD.set_title(labels[3])
