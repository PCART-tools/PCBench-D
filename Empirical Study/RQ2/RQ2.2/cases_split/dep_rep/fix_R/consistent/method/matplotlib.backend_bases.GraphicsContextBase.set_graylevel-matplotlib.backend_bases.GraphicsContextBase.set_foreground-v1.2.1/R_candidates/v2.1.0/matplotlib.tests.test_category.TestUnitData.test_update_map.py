    def test_update_map(self):
        data = ['a', 'd']
        oseq = ['a', 'd']
        olocs = [0, 1]

        data_update = ['b', 'd', 'e', np.inf]
        useq = ['a', 'd', 'b', 'e', 'inf']
        ulocs = [0, 1, 2, 3, -2]

        unitdata = cat.UnitData(data)
        assert unitdata.seq == oseq
        assert unitdata.locs == olocs

        unitdata.update(data_update)
        assert unitdata.seq == useq
        assert unitdata.locs == ulocs
