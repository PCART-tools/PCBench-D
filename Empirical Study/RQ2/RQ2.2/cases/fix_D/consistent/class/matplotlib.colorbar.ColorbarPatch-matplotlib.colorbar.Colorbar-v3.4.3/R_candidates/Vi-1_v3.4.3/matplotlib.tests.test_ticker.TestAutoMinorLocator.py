class TestAutoMinorLocator:
    def test_basic(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 1.39)
        ax.minorticks_on()
        test_value = np.array([0.05, 0.1, 0.15, 0.25, 0.3, 0.35, 0.45,
                               0.5, 0.55, 0.65, 0.7, 0.75, 0.85, 0.9,
                               0.95, 1.05, 1.1, 1.15, 1.25, 1.3, 1.35])
        assert_almost_equal(ax.xaxis.get_ticklocs(minor=True), test_value)

    # NB: the following values are assuming that *xlim* is [0, 5]
    params = [
        (0, 0),  # no major tick => no minor tick either
        (1, 0)   # a single major tick => no minor tick
    ]

    @pytest.mark.parametrize('nb_majorticks, expected_nb_minorticks', params)
    def test_low_number_of_majorticks(
            self, nb_majorticks, expected_nb_minorticks):
        # This test is related to issue #8804
        fig, ax = plt.subplots()
        xlims = (0, 5)  # easier to test the different code paths
        ax.set_xlim(*xlims)
        ax.set_xticks(np.linspace(xlims[0], xlims[1], nb_majorticks))
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
        assert len(ax.xaxis.get_minorticklocs()) == expected_nb_minorticks

    majorstep_minordivisions = [(1, 5),
                                (2, 4),
                                (2.5, 5),
                                (5, 5),
                                (10, 5)]

    # This test is meant to verify the parameterization for
    # test_number_of_minor_ticks
    def test_using_all_default_major_steps(self):
        with mpl.rc_context({'_internal.classic_mode': False}):
            majorsteps = [x[0] for x in self.majorstep_minordivisions]
            np.testing.assert_allclose(majorsteps,
                                       mticker.AutoLocator()._steps)

    @pytest.mark.parametrize('major_step, expected_nb_minordivisions',
                             majorstep_minordivisions)
    def test_number_of_minor_ticks(
            self, major_step, expected_nb_minordivisions):
        fig, ax = plt.subplots()
        xlims = (0, major_step)
        ax.set_xlim(*xlims)
        ax.set_xticks(xlims)
        ax.minorticks_on()
        ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
        nb_minor_divisions = len(ax.xaxis.get_minorticklocs()) + 1
        assert nb_minor_divisions == expected_nb_minordivisions

    limits = [(0, 1.39), (0, 0.139),
              (0, 0.11e-19), (0, 0.112e-12),
              (-2.0e-07, -3.3e-08), (1.20e-06, 1.42e-06),
              (-1.34e-06, -1.44e-06), (-8.76e-07, -1.51e-06)]

    reference = [
        [0.05, 0.1, 0.15, 0.25, 0.3, 0.35, 0.45, 0.5, 0.55, 0.65, 0.7,
         0.75, 0.85, 0.9, 0.95, 1.05, 1.1, 1.15, 1.25, 1.3, 1.35],
        [0.005, 0.01, 0.015, 0.025, 0.03, 0.035, 0.045, 0.05, 0.055, 0.065,
         0.07, 0.075, 0.085, 0.09, 0.095, 0.105, 0.11, 0.115, 0.125, 0.13,
         0.135],
        [5.00e-22, 1.00e-21, 1.50e-21, 2.50e-21, 3.00e-21, 3.50e-21, 4.50e-21,
         5.00e-21, 5.50e-21, 6.50e-21, 7.00e-21, 7.50e-21, 8.50e-21, 9.00e-21,
         9.50e-21, 1.05e-20, 1.10e-20],
        [5.00e-15, 1.00e-14, 1.50e-14, 2.50e-14, 3.00e-14, 3.50e-14, 4.50e-14,
         5.00e-14, 5.50e-14, 6.50e-14, 7.00e-14, 7.50e-14, 8.50e-14, 9.00e-14,
         9.50e-14, 1.05e-13, 1.10e-13],
        [-1.95e-07, -1.90e-07, -1.85e-07, -1.75e-07, -1.70e-07, -1.65e-07,
         -1.55e-07, -1.50e-07, -1.45e-07, -1.35e-07, -1.30e-07, -1.25e-07,
         -1.15e-07, -1.10e-07, -1.05e-07, -9.50e-08, -9.00e-08, -8.50e-08,
         -7.50e-08, -7.00e-08, -6.50e-08, -5.50e-08, -5.00e-08, -4.50e-08,
         -3.50e-08],
        [1.21e-06, 1.22e-06, 1.23e-06, 1.24e-06, 1.26e-06, 1.27e-06, 1.28e-06,
         1.29e-06, 1.31e-06, 1.32e-06, 1.33e-06, 1.34e-06, 1.36e-06, 1.37e-06,
         1.38e-06, 1.39e-06, 1.41e-06, 1.42e-06],
        [-1.435e-06, -1.430e-06, -1.425e-06, -1.415e-06, -1.410e-06,
         -1.405e-06, -1.395e-06, -1.390e-06, -1.385e-06, -1.375e-06,
         -1.370e-06, -1.365e-06, -1.355e-06, -1.350e-06, -1.345e-06],
        [-1.48e-06, -1.46e-06, -1.44e-06, -1.42e-06, -1.38e-06, -1.36e-06,
         -1.34e-06, -1.32e-06, -1.28e-06, -1.26e-06, -1.24e-06, -1.22e-06,
         -1.18e-06, -1.16e-06, -1.14e-06, -1.12e-06, -1.08e-06, -1.06e-06,
         -1.04e-06, -1.02e-06, -9.80e-07, -9.60e-07, -9.40e-07, -9.20e-07,
         -8.80e-07]]

    additional_data = list(zip(limits, reference))

    @pytest.mark.parametrize('lim, ref', additional_data)
    def test_additional(self, lim, ref):
        fig, ax = plt.subplots()

        ax.minorticks_on()
        ax.grid(True, 'minor', 'y', linewidth=1)
        ax.grid(True, 'major', color='k', linewidth=1)
        ax.set_ylim(lim)

        assert_almost_equal(ax.yaxis.get_ticklocs(minor=True), ref)
