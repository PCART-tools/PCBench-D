    @check_figures_equal(extensions=["png"])
    def test_nested_tuple(self, fig_test, fig_ref):
        x = [["A", "B", "B"], ["C", "C", "D"]]
        xt = (("A", "B", "B"), ("C", "C", "D"))

        fig_ref.subplot_mosaic([["F"], [x]])
        fig_test.subplot_mosaic([["F"], [xt]])
