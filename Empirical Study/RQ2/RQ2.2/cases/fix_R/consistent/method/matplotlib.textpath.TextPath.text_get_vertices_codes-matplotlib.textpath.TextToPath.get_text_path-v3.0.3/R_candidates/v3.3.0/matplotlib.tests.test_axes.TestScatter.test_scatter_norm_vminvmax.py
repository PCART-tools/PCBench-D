    @check_figures_equal(extensions=["png"])
    def test_scatter_norm_vminvmax(self, fig_test, fig_ref):
        """Parameters vmin, vmax should be ignored if norm is given."""
        x = [1, 2, 3]
        ax = fig_ref.subplots()
        ax.scatter(x, x, c=x, vmin=0, vmax=5)
        ax = fig_test.subplots()
        with pytest.warns(MatplotlibDeprecationWarning,
                          match="Passing parameters norm and vmin/vmax "
                                "simultaneously is deprecated."):
            ax.scatter(x, x, c=x, norm=mcolors.Normalize(-10, 10),
                       vmin=0, vmax=5)
