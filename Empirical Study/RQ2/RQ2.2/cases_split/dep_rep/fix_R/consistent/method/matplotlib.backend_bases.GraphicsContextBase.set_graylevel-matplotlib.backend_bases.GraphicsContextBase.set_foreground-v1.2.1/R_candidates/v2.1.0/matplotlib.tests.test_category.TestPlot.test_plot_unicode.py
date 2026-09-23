    def test_plot_unicode(self):
        words = ['Здравствуйте', 'привет']
        locs = [0.0, 1.0]
        unit_data = MockUnitData(zip(words, locs))

        fig, ax = plt.subplots()
        ax.plot(words)
        fig.canvas.draw()

        self.axis_test(ax.yaxis, locs, words, unit_data)
