    @check_figures_equal(extensions=["png"])
    def test_scatter_decimal(self, fig_test, fig_ref):
        x0 = np.array([1.5, 8.4, 5.3, 4.2])
        y0 = np.array([1.1, 2.2, 3.3, 4.4])
        x = np.array([Decimal(i) for i in x0])
        y = np.array([Decimal(i) for i in y0])
        c = ['r', 'y', 'b', 'lime']
        s = [24, 15, 19, 29]
        # Test image - scatter plot with Decimal() input
        ax = fig_test.subplots()
        ax.scatter(x, y, c=c, s=s)
        # Reference image
        ax = fig_ref.subplots()
        ax.scatter(x0, y0, c=c, s=s)
