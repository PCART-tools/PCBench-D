    def test_warn_args_kwargs(self):
        fig, axs = plt.subplots(1, 2)
        lines = axs[0].plot(range(10))
        lines2 = axs[1].plot(np.arange(10) * 2.)
        with mock.patch('warnings.warn') as warn:
            fig.legend((lines, lines2), labels=('a', 'b'))
        warn.assert_called_with("You have mixed positional and keyword "
                                "arguments, some input may be "
                                "discarded.")
