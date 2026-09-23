    def test_legend_kwargs_handles_only(self):
        fig, ax = plt.subplots()
        x = np.linspace(0, 1, 11)
        ln1, = ax.plot(x, x, label='x')
        ln2, = ax.plot(x, 2*x, label='2x')
        ln3, = ax.plot(x, 3*x, label='3x')
        with mock.patch('matplotlib.legend.Legend') as Legend:
            ax.legend(handles=[ln3, ln2])  # reversed and not ln1
        Legend.assert_called_with(ax, [ln3, ln2], ['3x', '2x'])
