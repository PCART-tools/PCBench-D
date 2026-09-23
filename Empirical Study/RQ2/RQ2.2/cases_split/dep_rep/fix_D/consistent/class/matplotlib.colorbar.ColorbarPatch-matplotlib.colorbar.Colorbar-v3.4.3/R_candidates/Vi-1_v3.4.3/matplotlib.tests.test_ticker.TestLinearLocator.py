class TestLinearLocator:
    def test_basic(self):
        loc = mticker.LinearLocator(numticks=3)
        test_value = np.array([-0.8, -0.3, 0.2])
        assert_almost_equal(loc.tick_values(-0.8, 0.2), test_value)

    def test_set_params(self):
        """
        Create linear locator with presets={}, numticks=2 and change it to
        something else. See if change was successful. Should not exception.
        """
        loc = mticker.LinearLocator(numticks=2)
        loc.set_params(numticks=8, presets={(0, 1): []})
        assert loc.numticks == 8
        assert loc.presets == {(0, 1): []}
