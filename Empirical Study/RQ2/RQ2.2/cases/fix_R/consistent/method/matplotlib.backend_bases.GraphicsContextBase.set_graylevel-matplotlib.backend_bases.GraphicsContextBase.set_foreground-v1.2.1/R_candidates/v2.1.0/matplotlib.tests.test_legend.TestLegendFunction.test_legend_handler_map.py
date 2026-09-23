    def test_legend_handler_map(self):
        lines = plt.plot(range(10), label='hello world')
        with mock.patch('matplotlib.axes.Axes.'
                        'get_legend_handles_labels') as handles_labels:
            handles_labels.return_value = lines, ['hello world']
            plt.legend(handler_map={'1': 2})
        handles_labels.assert_called_with({'1': 2})
