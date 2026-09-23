    @check_figures_equal(extensions=["png"])
    def test_scatter_no_invalid_color(self, fig_test, fig_ref):
        # With plotnonfinite=False we plot only 2 points.
        ax = fig_test.subplots()
        cmap = mpl.colormaps["viridis"].resampled(16)
        cmap.set_bad("k", 1)
        ax.scatter(range(4), range(4),
                   c=[1, np.nan, 2, np.nan], s=[1, 2, 3, 4],
                   cmap=cmap, plotnonfinite=False)
        ax = fig_ref.subplots()
        ax.scatter([0, 2], [0, 2], c=[1, 2], s=[1, 3], cmap=cmap)
