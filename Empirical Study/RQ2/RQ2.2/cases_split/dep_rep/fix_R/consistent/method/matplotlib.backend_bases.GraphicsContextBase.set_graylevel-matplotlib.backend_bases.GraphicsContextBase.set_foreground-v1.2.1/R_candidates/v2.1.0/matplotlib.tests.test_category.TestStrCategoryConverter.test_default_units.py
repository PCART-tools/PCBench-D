    def test_default_units(self):
        axis = FakeAxis(None)
        assert self.cc.default_units(["a"], axis) is None
