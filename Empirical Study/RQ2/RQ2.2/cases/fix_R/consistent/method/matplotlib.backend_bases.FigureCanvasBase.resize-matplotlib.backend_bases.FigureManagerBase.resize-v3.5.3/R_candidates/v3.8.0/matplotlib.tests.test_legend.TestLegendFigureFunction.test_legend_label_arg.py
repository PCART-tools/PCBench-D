    def test_legend_label_arg(self):
        fig, ax = plt.subplots()
        lines = ax.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            fig.legend(['foobar'])
        Legend.assert_called_with(fig, lines, ['foobar'],
                                  bbox_transform=fig.transFigure)
