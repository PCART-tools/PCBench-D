    def test_legend_kwargs_labels_only(self):
        fig, ax = plt.subplots()
        x = np.linspace(0, 1, 11)
        ln1, = ax.plot(x, x)
        ln2, = ax.plot(x, 2*x)
        with mock.patch('matplotlib.legend.Legend') as Legend:
            ax.legend(labels=['x', '2x'])
        Legend.assert_called_with(ax, [ln1, ln2], ['x', '2x'])
