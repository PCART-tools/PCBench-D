    @pytest.mark.parametrize('value, long, short', [
        (0.0, "0", "0           "),
        (0, "0", "0           "),
        (-1.0, "-10^0", "-1          "),
        (2e-10, "2x10^-10", "2e-10       "),
        (1e10, "10^10", "1e+10       "),
    ])
    def test_format_data(self, value, long, short):
        fig, ax = plt.subplots()
        ax.set_xscale('log')
        fmt = ax.xaxis.get_major_formatter()
        assert fmt.format_data(value) == long
        assert fmt.format_data_short(value) == short
