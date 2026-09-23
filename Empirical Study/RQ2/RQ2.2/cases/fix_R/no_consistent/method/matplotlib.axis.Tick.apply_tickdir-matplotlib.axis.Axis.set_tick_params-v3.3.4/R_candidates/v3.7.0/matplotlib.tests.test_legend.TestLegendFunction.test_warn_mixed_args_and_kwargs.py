    def test_warn_mixed_args_and_kwargs(self):
        fig, ax = plt.subplots()
        th = np.linspace(0, 2*np.pi, 1024)
        lns, = ax.plot(th, np.sin(th), label='sin')
        lnc, = ax.plot(th, np.cos(th), label='cos')
        with pytest.warns(UserWarning) as record:
            ax.legend((lnc, lns), labels=('a', 'b'))
        assert len(record) == 1
        assert str(record[0].message) == (
            "You have mixed positional and keyword arguments, some input may "
            "be discarded.")
