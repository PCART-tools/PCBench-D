    @pytest.mark.usefixtures("data")
    @pytest.mark.parametrize("bars", bytes_data, ids=bytes_ids)
    def test_plot_bytes(self, bars):
        counts = np.array([4, 6, 5])

        fig, ax = plt.subplots()
        ax.bar(bars, counts)
        fig.canvas.draw()

        self.axis_test(ax.xaxis, self.dticks, self.dlabels, self.dunit_data)
