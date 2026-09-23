    @pytest.mark.parametrize("ydata", cases, ids=ids)
    def test_StrCategoryFormatter(self, ax, ydata):
        unit = cat.UnitData(ydata)
        labels = cat.StrCategoryFormatter(unit._mapping)
        for i, d in enumerate(ydata):
            assert labels(i, i) == _to_str(d)
