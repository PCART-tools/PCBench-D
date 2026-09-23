    @pytest.mark.parametrize('data, expected', cursor_data)
    def test_cursor_precision(self, data, expected):
        fig, ax = plt.subplots()
        ax.set_xlim(-1, 1)  # Pointing precision of 0.001.
        fmt = ax.xaxis.get_major_formatter().format_data_short
        assert fmt(data) == expected
