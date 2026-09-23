    def test_set_params(self):
        """
        Create multiple locator with 0.7 base, and change it to something else.
        See if change was successful.
        """
        mult = mticker.MultipleLocator(base=0.7)
        mult.set_params(base=1.7)
        assert mult._edge.step == 1.7
        mult.set_params(offset=3)
        assert mult._offset == 3
