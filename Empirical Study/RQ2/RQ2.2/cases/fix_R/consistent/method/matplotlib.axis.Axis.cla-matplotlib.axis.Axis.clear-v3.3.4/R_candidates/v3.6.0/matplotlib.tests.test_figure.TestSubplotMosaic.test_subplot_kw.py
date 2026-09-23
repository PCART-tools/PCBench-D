    @check_figures_equal(extensions=["png"])
    @pytest.mark.parametrize("subplot_kw", [{}, {"projection": "polar"}, None])
    def test_subplot_kw(self, fig_test, fig_ref, subplot_kw):
        x = [[1, 2]]
        grid_axes = fig_test.subplot_mosaic(x, subplot_kw=subplot_kw)
        subplot_kw = subplot_kw or {}

        gs = fig_ref.add_gridspec(1, 2)
        axA = fig_ref.add_subplot(gs[0, 0], **subplot_kw)

        axB = fig_ref.add_subplot(gs[0, 1], **subplot_kw)
