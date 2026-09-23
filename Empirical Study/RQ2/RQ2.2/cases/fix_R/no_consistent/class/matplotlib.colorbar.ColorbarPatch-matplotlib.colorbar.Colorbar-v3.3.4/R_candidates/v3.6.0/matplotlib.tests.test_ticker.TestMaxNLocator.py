class TestMaxNLocator:
    basic_data = [
        (20, 100, np.array([20., 40., 60., 80., 100.])),
        (0.001, 0.0001, np.array([0., 0.0002, 0.0004, 0.0006, 0.0008, 0.001])),
        (-1e15, 1e15, np.array([-1.0e+15, -5.0e+14, 0e+00, 5e+14, 1.0e+15])),
        (0, 0.85e-50, np.arange(6) * 2e-51),
        (-0.85e-50, 0, np.arange(-5, 1) * 2e-51),
    ]

    integer_data = [
        (-0.1, 1.1, None, np.array([-1, 0, 1, 2])),
        (-0.1, 0.95, None, np.array([-0.25, 0, 0.25, 0.5, 0.75, 1.0])),
        (1, 55, [1, 1.5, 5, 6, 10], np.array([0, 15, 30, 45, 60])),
    ]

    @pytest.mark.parametrize('vmin, vmax, expected', basic_data)
    def test_basic(self, vmin, vmax, expected):
        loc = mticker.MaxNLocator(nbins=5)
        assert_almost_equal(loc.tick_values(vmin, vmax), expected)

    @pytest.mark.parametrize('vmin, vmax, steps, expected', integer_data)
    def test_integer(self, vmin, vmax, steps, expected):
        loc = mticker.MaxNLocator(nbins=5, integer=True, steps=steps)
        assert_almost_equal(loc.tick_values(vmin, vmax), expected)
