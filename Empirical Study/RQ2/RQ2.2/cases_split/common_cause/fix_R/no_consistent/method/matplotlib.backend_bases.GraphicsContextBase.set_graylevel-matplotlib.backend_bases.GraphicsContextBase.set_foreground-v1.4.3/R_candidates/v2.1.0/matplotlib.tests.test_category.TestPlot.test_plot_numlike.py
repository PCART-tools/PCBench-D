    @pytest.mark.parametrize("bars", numlike_data, ids=numlike_ids)
    def test_plot_numlike(self, bars):
        counts = np.array([4, 6, 5])

        fig, ax = plt.subplots()
        ax.bar(bars, counts)
        fig.canvas.draw()

        unitmap = MockUnitData([('1', 0), ('11', 1), ('3', 2)])
        self.axis_test(ax.xaxis, [0, 1, 2], ['1', '11', '3'], unitmap)
