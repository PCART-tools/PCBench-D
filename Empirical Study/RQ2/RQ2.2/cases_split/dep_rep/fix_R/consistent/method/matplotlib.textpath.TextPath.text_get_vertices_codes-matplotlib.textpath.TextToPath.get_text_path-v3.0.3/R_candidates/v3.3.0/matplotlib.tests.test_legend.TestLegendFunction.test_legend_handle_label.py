    def test_legend_handle_label(self):
        lines = plt.plot(range(10))
        with mock.patch('matplotlib.legend.Legend') as Legend:
            plt.legend(lines, ['hello world'])
        Legend.assert_called_with(plt.gca(), lines, ['hello world'])
