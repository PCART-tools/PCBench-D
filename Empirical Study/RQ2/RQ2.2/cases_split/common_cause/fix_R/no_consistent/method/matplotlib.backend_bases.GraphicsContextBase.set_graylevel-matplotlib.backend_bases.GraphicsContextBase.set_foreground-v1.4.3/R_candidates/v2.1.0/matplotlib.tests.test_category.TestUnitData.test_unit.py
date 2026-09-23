    @pytest.mark.parametrize("data, seq, locs", testdata, ids=ids)
    def test_unit(self, data, seq, locs):
        act = cat.UnitData(data)
        assert act.seq == seq
        assert act.locs == locs
