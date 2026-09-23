    def addError(self, test, err, *zero_nine_capt_args):
        # Fixme (Really weird): if I don't leave empty method here,
        # nose gets confused and KnownFails become testing errors when
        # using the MplNosePlugin and MplTestCase.

        # The *zero_nine_capt_args captures an extra argument. There
        # seems to be a bug in
        # nose.testing.manager.ZeroNinePlugin.addError() in which a
        # 3rd positional argument ("capt") is passed to the plugin's
        # addError() method, even if one is not explicitly using the
        # ZeroNinePlugin.
        pass
