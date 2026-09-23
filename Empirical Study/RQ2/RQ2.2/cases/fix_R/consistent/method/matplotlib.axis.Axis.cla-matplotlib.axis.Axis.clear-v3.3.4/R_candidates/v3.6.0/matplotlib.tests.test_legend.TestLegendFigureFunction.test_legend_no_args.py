    def test_legend_no_args(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10), label='hello world')
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend()
        Legend.assert_called_with(fig, lines, ['hello world'],
                                  bbox_transform=fig.transFigure)
