    @pytest.mark.parametrize("N", (100, 253, 754))
    def test_format_data_short(self, N):
        locs = np.linspace(0, 1, N)[1:-1]
        form = mticker.LogitFormatter()
        for x in locs:
            fx = form.format_data_short(x)
            if fx.startswith("1-"):
                x2 = 1 - float(fx[2:])
            else:
                x2 = float(fx)
            assert np.abs(x - x2) < 1 / N
