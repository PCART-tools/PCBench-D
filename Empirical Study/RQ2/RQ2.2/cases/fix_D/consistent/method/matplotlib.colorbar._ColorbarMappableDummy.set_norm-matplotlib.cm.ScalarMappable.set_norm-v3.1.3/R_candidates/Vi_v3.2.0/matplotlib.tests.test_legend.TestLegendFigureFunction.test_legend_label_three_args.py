    def test_legend_label_three_args(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(lines, ['foobar'], 'right')
        Legend.assert_called_with(fig, lines, ['foobar'], 'right')
