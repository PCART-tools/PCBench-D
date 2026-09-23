    def test_share_all(self):
        layout = [
            ["A", [["B", "C"],
                   ["D", "E"]]],
            ["F", "G"],
            [".", [["H", [["I"],
                          ["."]]]]]
        ]
        fig = plt.figure()
        ax_dict = fig.subplot_mosaic(layout, sharex=True, sharey=True)
        ax_dict["A"].set(xscale="log", yscale="logit")
        assert all(ax.get_xscale() == "log" and ax.get_yscale() == "logit"
                   for ax in ax_dict.values())
