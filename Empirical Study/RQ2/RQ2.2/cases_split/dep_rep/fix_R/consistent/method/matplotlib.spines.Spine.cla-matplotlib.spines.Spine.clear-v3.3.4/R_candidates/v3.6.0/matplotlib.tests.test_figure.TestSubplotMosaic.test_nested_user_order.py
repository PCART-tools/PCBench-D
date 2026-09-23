    def test_nested_user_order(self):
        layout = [
            ["A", [["B", "C"],
                   ["D", "E"]]],
            ["F", "G"],
            [".", [["H", [["I"],
                          ["."]]]]]
        ]

        fig = plt.figure()
        ax_dict = fig.subplot_mosaic(layout)
        assert list(ax_dict) == list("ABCDEFGHI")
        assert list(fig.axes) == list(ax_dict.values())
