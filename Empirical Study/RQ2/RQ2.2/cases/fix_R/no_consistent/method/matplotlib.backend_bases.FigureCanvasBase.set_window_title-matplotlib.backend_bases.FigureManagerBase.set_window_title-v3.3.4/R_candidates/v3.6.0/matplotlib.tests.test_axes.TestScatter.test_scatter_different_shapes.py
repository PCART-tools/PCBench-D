    @check_figures_equal(extensions=["png"])
    def test_scatter_different_shapes(self, fig_test, fig_ref):
        x = np.arange(10)
        ax = fig_test.subplots()
        ax.scatter(x, x.reshape(2, 5), c=x.reshape(5, 2))
        ax = fig_ref.subplots()
        ax.scatter(x.reshape(5, 2), x, c=x.reshape(2, 5))
