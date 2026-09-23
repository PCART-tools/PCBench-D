    @check_figures_equal(extensions=["png"])
    @pytest.mark.parametrize("str_pattern",
                             ["AAA\nBBB", "\nAAA\nBBB\n", "ABC\nDEF"]
                             )
    def test_single_str_input(self, fig_test, fig_ref, str_pattern):
        grid_axes = fig_test.subplot_mosaic(str_pattern)

        grid_axes = fig_ref.subplot_mosaic(
            [list(ln) for ln in str_pattern.strip().split("\n")]
        )
