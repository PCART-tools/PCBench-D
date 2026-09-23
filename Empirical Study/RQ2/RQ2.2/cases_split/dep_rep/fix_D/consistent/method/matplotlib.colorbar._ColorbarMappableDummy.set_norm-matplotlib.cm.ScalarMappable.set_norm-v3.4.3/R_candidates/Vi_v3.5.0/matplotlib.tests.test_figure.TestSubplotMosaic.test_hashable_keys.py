    @check_figures_equal(extensions=["png"])
    def test_hashable_keys(self, fig_test, fig_ref):
        fig_test.subplot_mosaic([[object(), object()]])
        fig_ref.subplot_mosaic([["A", "B"]])
