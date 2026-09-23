    def test_legend_handle_label(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(lines, ['hello world'])
        Legend.assert_called_with(fig, lines, ['hello world'])
