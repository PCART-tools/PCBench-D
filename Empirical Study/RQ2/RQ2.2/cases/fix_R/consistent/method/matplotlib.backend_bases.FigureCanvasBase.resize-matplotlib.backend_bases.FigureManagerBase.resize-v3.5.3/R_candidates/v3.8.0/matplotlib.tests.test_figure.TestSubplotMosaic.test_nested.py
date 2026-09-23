    @check_figures_equal(extensions=["png"])
    def test_nested(self, fig_test, fig_ref):

        fig_ref.set_layout_engine("constrained")
        fig_test.set_layout_engine("constrained")

        x = [["A", "B"], ["C", "D"]]

        y = [["F"], [x]]

        grid_axes = fig_test.subplot_mosaic(y)

        for k, ax in grid_axes.items():
            ax.set_title(k)

        gs = fig_ref.add_gridspec(2, 1)

        gs_n = gs[1, 0].subgridspec(2, 2)

        axA = fig_ref.add_subplot(gs_n[0, 0])
        axA.set_title("A")

        axB = fig_ref.add_subplot(gs_n[0, 1])
        axB.set_title("B")

        axC = fig_ref.add_subplot(gs_n[1, 0])
        axC.set_title("C")

        axD = fig_ref.add_subplot(gs_n[1, 1])
        axD.set_title("D")

        axF = fig_ref.add_subplot(gs[0, 0])
        axF.set_title("F")
