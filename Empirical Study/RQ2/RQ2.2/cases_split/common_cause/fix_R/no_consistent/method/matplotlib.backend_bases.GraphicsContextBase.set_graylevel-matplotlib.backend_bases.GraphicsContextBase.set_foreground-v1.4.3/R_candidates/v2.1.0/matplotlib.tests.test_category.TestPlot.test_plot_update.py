    def test_plot_update(self):
        fig, ax = plt.subplots()

        ax.plot(['a', 'b'])
        ax.plot(['a', 'b', 'd'])
        ax.plot(['b', 'c', 'd'])
        fig.canvas.draw()

        labels = ['a', 'b', 'd', 'c']
        ticks = [0, 1, 2, 3]
        unit_data = MockUnitData(list(zip(labels, ticks)))

        self.axis_test(ax.yaxis, ticks, labels, unit_data)
