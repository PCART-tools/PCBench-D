    def test_axisinfo(self):
        axis = self.cc.axisinfo(self.unit, self.ax)
        assert isinstance(axis.majloc, cat.StrCategoryLocator)
        assert isinstance(axis.majfmt, cat.StrCategoryFormatter)
