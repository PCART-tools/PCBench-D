    @pytest.mark.parametrize("data, locs", data, ids=ids)
    def test_unit(self, data, locs):
        unit = cat.UnitData(data)
        assert list(unit._mapping.keys()) == data
        assert list(unit._mapping.values()) == locs
