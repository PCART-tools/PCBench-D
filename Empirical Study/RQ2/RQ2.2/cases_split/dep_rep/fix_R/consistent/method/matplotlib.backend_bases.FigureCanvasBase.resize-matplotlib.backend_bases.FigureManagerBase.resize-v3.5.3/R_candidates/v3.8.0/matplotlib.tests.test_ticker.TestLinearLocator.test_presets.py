    def test_presets(self):
        loc = mticker.LinearLocator(presets={(1, 2): [1, 1.25, 1.75],
                                             (0, 2): [0.5, 1.5]})
        assert loc.tick_values(1, 2) == [1, 1.25, 1.75]
        assert loc.tick_values(2, 1) == [1, 1.25, 1.75]
        assert loc.tick_values(0, 2) == [0.5, 1.5]
        assert loc.tick_values(0.0, 2.0) == [0.5, 1.5]
        assert (loc.tick_values(0, 1) == np.linspace(0, 1, 11)).all()
