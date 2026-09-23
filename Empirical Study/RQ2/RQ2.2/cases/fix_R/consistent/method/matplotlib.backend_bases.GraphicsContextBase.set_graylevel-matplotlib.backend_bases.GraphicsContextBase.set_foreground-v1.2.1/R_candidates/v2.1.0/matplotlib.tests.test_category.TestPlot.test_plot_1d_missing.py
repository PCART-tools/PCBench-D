    @pytest.mark.usefixtures("missing_data")
    def test_plot_1d_missing(self):
        fig, ax = plt.subplots()
        ax.plot(self.dm)
        fig.canvas.draw()

        self.axis_test(ax.yaxis, self.dmticks, self.dmlabels, self.dmunit_data)
