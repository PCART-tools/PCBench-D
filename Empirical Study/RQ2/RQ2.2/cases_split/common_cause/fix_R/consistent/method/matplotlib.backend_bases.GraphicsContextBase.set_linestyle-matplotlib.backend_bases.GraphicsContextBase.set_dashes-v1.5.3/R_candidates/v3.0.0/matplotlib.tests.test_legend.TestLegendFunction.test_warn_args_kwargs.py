    def test_warn_args_kwargs(self):
        fig, ax = plt.subplots(1, 1)
        th = np.linspace(0, 2*np.pi, 1024)
        lns, = ax.plot(th, np.sin(th), label='sin', lw=5)
        lnc, = ax.plot(th, np.cos(th), label='cos', lw=5)
        with mock.patch('warnings.warn') as warn:
            ax.legend((lnc, lns), labels=('a', 'b'))

        warn.assert_called_with("You have mixed positional and keyword "
                                "arguments, some input may be "
                                "discarded.")
