    @check_figures_equal(extensions=["png"])
    @pytest.mark.parametrize("multi_value", ['BC', tuple('BC')])
    def test_per_subplot_kw(self, fig_test, fig_ref, multi_value):
        x = 'AB;CD'
        grid_axes = fig_test.subplot_mosaic(
            x,
            subplot_kw={'facecolor': 'red'},
            per_subplot_kw={
                'D': {'facecolor': 'blue'},
                multi_value: {'facecolor': 'green'},
            }
        )

        gs = fig_ref.add_gridspec(2, 2)
        for color, spec in zip(['red', 'green', 'green', 'blue'], gs):
            fig_ref.add_subplot(spec, facecolor=color)
