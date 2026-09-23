    @check_figures_equal(extensions=["png"])
    @pytest.mark.parametrize(
        "x, empty_sentinel",
        [
            ([["A", None], [None, "B"]], None),
            ([["A", "."], [".", "B"]], "SKIP"),
            ([["A", 0], [0, "B"]], 0),
            ([[1, None], [None, 2]], None),
            ([[1, "."], [".", 2]], "SKIP"),
            ([[1, 0], [0, 2]], 0),
        ],
    )
    def test_empty(self, fig_test, fig_ref, x, empty_sentinel):
        if empty_sentinel != "SKIP":
            kwargs = {"empty_sentinel": empty_sentinel}
        else:
            kwargs = {}
        grid_axes = fig_test.subplot_mosaic(x, **kwargs)

        for k, ax in grid_axes.items():
            ax.set_title(k)

        labels = sorted(
            {name for row in x for name in row} - {empty_sentinel, "."}
        )

        assert len(labels) == len(grid_axes)

        gs = fig_ref.add_gridspec(2, 2)
        axA = fig_ref.add_subplot(gs[0, 0])
        axA.set_title(labels[0])

        axB = fig_ref.add_subplot(gs[1, 1])
        axB.set_title(labels[1])
