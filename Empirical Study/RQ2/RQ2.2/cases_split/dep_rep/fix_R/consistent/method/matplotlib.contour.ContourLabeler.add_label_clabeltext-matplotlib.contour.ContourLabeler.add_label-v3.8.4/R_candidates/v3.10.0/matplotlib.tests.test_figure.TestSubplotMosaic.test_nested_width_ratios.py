    def test_nested_width_ratios(self):
        x = [["A", [["B"],
                    ["C"]]]]
        width_ratios = [2, 1]

        fig, axd = plt.subplot_mosaic(x, width_ratios=width_ratios)

        assert axd["A"].get_gridspec().get_width_ratios() == width_ratios
        assert axd["B"].get_gridspec().get_width_ratios() != width_ratios
