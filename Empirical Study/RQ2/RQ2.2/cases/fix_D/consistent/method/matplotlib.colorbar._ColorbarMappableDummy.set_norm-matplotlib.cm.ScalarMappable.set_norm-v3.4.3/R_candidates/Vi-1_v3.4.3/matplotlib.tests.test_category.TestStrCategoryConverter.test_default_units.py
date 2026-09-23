    def test_default_units(self):
        assert isinstance(self.cc.default_units(["a"], self.ax), cat.UnitData)
