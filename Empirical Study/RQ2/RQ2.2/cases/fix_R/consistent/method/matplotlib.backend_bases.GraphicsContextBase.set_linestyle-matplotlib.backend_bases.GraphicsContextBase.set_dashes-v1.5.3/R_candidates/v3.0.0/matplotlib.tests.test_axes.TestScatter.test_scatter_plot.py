    @image_comparison(baseline_images=['scatter', 'scatter'])
    def test_scatter_plot(self):
        fig, ax = plt.subplots()
        data = {"x": [3, 4, 2, 6], "y": [2, 5, 2, 3],
                "c": ['r', 'y', 'b', 'lime'], "s": [24, 15, 19, 29]}

        ax.scatter(data["x"], data["y"], c=data["c"], s=data["s"])

        # Reuse testcase from above for a labeled data test
        fig, ax = plt.subplots()
        ax.scatter("x", "y", c="c", s="s", data=data)
