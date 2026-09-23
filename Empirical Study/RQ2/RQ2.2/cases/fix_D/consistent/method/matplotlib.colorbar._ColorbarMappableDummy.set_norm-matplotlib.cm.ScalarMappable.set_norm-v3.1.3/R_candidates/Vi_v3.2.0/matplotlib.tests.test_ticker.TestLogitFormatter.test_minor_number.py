    def test_minor_number(self):
        """
        Test the parameter minor_number
        """
        min_loc = mticker.LogitLocator(minor=True)
        min_form = mticker.LogitFormatter(minor=True)
        ticks = min_loc.tick_values(5e-2, 1 - 5e-2)
        for minor_number in (2, 4, 8, 16):
            min_form.set_minor_number(minor_number)
            formatted = min_form.format_ticks(ticks)
            labelled = [f for f in formatted if len(f) > 0]
            assert len(labelled) == minor_number
