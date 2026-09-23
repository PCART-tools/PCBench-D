    @image_comparison(baseline_images=['scatter'],
                      style='mpl20', remove_text=True)
    def test_scatter_plot(self):
        data = {"x": np.array([3, 4, 2, 6]), "y": np.array([2, 5, 2, 3]),
                "c": ['r', 'y', 'b', 'lime'], "s": [24, 15, 19, 29],
                "c2": ['0.5', '0.6', '0.7', '0.8']}

        fig, ax = plt.subplots()
        ax.scatter(data["x"] - 1., data["y"] - 1., c=data["c"], s=data["s"])
        ax.scatter(data["x"] + 1., data["y"] + 1., c=data["c2"], s=data["s"])
        ax.scatter("x", "y", c="c", s="s", data=data)
