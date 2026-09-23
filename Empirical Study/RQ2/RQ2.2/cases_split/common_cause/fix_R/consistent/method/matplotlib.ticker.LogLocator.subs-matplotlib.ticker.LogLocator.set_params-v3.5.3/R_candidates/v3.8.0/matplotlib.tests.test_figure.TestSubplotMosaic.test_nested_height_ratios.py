    def test_nested_height_ratios(self):
        x = [["A", [["B"],
                    ["C"]]], ["D", "D"]]
        height_ratios = [1, 2]

        fig, axd = plt.subplot_mosaic(x, height_ratios=height_ratios)

        assert axd["D"].get_gridspec().get_height_ratios() == height_ratios
        assert axd["B"].get_gridspec().get_height_ratios() != height_ratios
