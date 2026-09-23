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
