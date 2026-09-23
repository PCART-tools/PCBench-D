class TestIndexLocator:
    def test_set_params(self):
        """
        Create index locator with 3 base, 4 offset. and change it to something
        else. See if change was successful.
        Should not exception.
        """
        index = mticker.IndexLocator(base=3, offset=4)
        index.set_params(base=7, offset=7)
        assert index._base == 7
        assert index.offset == 7
