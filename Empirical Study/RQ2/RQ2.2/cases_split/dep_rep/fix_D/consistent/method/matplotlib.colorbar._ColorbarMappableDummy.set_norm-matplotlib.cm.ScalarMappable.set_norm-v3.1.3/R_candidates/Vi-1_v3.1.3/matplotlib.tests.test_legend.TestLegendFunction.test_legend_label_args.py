    def test_legend_label_args(self):
        lines = plt.plot(range(10), label='hello world')
        with mock.patch('matplotlib.legend.Legend') as Legend:
            plt.legend(['foobar'])
        Legend.assert_called_with(plt.gca(), lines, ['foobar'])
