class TestLogitLocator:
    ref_basic_limits = [
        (5e-2, 1 - 5e-2),
        (5e-3, 1 - 5e-3),
        (5e-4, 1 - 5e-4),
        (5e-5, 1 - 5e-5),
        (5e-6, 1 - 5e-6),
        (5e-7, 1 - 5e-7),
        (5e-8, 1 - 5e-8),
        (5e-9, 1 - 5e-9),
    ]

    ref_basic_major_ticks = [
        1 / (10 ** np.arange(1, 3)),
        1 / (10 ** np.arange(1, 4)),
        1 / (10 ** np.arange(1, 5)),
        1 / (10 ** np.arange(1, 6)),
        1 / (10 ** np.arange(1, 7)),
        1 / (10 ** np.arange(1, 8)),
        1 / (10 ** np.arange(1, 9)),
        1 / (10 ** np.arange(1, 10)),
    ]

    ref_maxn_limits = [(0.4, 0.6), (5e-2, 2e-1), (1 - 2e-1, 1 - 5e-2)]

    @pytest.mark.parametrize(
        "lims, expected_low_ticks",
        zip(ref_basic_limits, ref_basic_major_ticks),
    )
    def test_basic_major(self, lims, expected_low_ticks):
        """
        Create logit locator with huge number of major, and tests ticks.
        """
        expected_ticks = sorted(
            [*expected_low_ticks, 0.5, *(1 - expected_low_ticks)]
        )
        loc = mticker.LogitLocator(nbins=100)
        _LogitHelper.assert_almost_equal(
            loc.tick_values(*lims),
            expected_ticks
        )

    @pytest.mark.parametrize("lims", ref_maxn_limits)
    def test_maxn_major(self, lims):
        """
        When the axis is zoomed, the locator must have the same behavior as
        MaxNLocator.
        """
        loc = mticker.LogitLocator(nbins=100)
        maxn_loc = mticker.MaxNLocator(nbins=100, steps=[1, 2, 5, 10])
        for nbins in (4, 8, 16):
            loc.set_params(nbins=nbins)
            maxn_loc.set_params(nbins=nbins)
            ticks = loc.tick_values(*lims)
            maxn_ticks = maxn_loc.tick_values(*lims)
            assert ticks.shape == maxn_ticks.shape
            assert (ticks == maxn_ticks).all()

    @pytest.mark.parametrize("lims", ref_basic_limits + ref_maxn_limits)
    def test_nbins_major(self, lims):
        """
        Assert logit locator for respecting nbins param.
        """

        basic_needed = int(-np.floor(np.log10(lims[0]))) * 2 + 1
        loc = mticker.LogitLocator(nbins=100)
        for nbins in range(basic_needed, 2, -1):
            loc.set_params(nbins=nbins)
            assert len(loc.tick_values(*lims)) <= nbins + 2

    @pytest.mark.parametrize(
        "lims, expected_low_ticks",
        zip(ref_basic_limits, ref_basic_major_ticks),
    )
    def test_minor(self, lims, expected_low_ticks):
        """
        In large scale, test the presence of minor,
        and assert no minor when major are subsampled.
        """

        expected_ticks = sorted(
            [*expected_low_ticks, 0.5, *(1 - expected_low_ticks)]
        )
        basic_needed = len(expected_ticks)
        loc = mticker.LogitLocator(nbins=100)
        minor_loc = mticker.LogitLocator(nbins=100, minor=True)
        for nbins in range(basic_needed, 2, -1):
            loc.set_params(nbins=nbins)
            minor_loc.set_params(nbins=nbins)
            major_ticks = loc.tick_values(*lims)
            minor_ticks = minor_loc.tick_values(*lims)
            if len(major_ticks) >= len(expected_ticks):
                # no subsample, we must have a lot of minors ticks
                assert (len(major_ticks) - 1) * 5 < len(minor_ticks)
            else:
                # subsample
                _LogitHelper.assert_almost_equal(
                    sorted([*major_ticks, *minor_ticks]), expected_ticks)

    def test_minor_attr(self):
        loc = mticker.LogitLocator(nbins=100)
        assert not loc.minor
        loc.minor = True
        assert loc.minor
        loc.set_params(minor=False)
        assert not loc.minor

    acceptable_vmin_vmax = [
        *(2.5 ** np.arange(-3, 0)),
        *(1 - 2.5 ** np.arange(-3, 0)),
    ]

    @pytest.mark.parametrize(
        "lims",
        [
            (a, b)
            for (a, b) in itertools.product(acceptable_vmin_vmax, repeat=2)
            if a != b
        ],
    )
    def test_nonsingular_ok(self, lims):
        """
        Create logit locator, and test the nonsingular method for acceptable
        value
        """
        loc = mticker.LogitLocator()
        lims2 = loc.nonsingular(*lims)
        assert sorted(lims) == sorted(lims2)

    @pytest.mark.parametrize("okval", acceptable_vmin_vmax)
    def test_nonsingular_nok(self, okval):
        """
        Create logit locator, and test the nonsingular method for non
        acceptable value
        """
        loc = mticker.LogitLocator()
        vmin, vmax = (-1, okval)
        vmin2, vmax2 = loc.nonsingular(vmin, vmax)
        assert vmax2 == vmax
        assert 0 < vmin2 < vmax2
        vmin, vmax = (okval, 2)
        vmin2, vmax2 = loc.nonsingular(vmin, vmax)
        assert vmin2 == vmin
        assert vmin2 < vmax2 < 1
