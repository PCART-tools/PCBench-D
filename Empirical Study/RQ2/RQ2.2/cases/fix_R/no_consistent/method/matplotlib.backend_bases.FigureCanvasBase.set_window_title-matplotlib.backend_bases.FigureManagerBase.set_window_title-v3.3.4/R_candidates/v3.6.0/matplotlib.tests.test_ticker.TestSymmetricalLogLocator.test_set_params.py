    def test_set_params(self):
        """
        Create symmetrical log locator with default subs =[1.0] numticks = 15,
        and change it to something else.
        See if change was successful.
        Should not exception.
        """
        sym = mticker.SymmetricalLogLocator(base=10, linthresh=1)
        sym.set_params(subs=[2.0], numticks=8)
        assert sym._subs == [2.0]
        assert sym.numticks == 8
