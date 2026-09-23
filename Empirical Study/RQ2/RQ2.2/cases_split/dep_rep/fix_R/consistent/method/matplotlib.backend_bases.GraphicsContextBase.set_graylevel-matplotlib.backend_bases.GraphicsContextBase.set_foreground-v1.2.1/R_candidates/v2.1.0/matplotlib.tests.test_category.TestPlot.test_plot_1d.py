    @pytest.mark.usefixtures("data")
    def test_plot_1d(self):
        fig, ax = plt.subplots()
        ax.plot(self.d)
        fig.canvas.draw()

        self.axis_test(ax.yaxis, self.dticks, self.dlabels, self.dunit_data)
