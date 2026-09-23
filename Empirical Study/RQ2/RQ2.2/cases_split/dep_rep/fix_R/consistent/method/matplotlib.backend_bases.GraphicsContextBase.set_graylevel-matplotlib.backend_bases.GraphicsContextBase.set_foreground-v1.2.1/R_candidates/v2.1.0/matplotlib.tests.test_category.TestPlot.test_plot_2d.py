    @pytest.mark.usefixtures("data", "missing_data")
    def test_plot_2d(self):
        fig, ax = plt.subplots()
        ax.plot(self.dm, self.d)
        fig.canvas.draw()

        self.axis_test(ax.xaxis, self.dmticks, self.dmlabels, self.dmunit_data)
        self.axis_test(ax.yaxis, self.dticks, self.dlabels, self.dunit_data)
