    def test_update(self):
        data = ['a', 'd']
        locs = [0, 1]

        data_update = ['b', 'd', 'e']
        unique_data = ['a', 'd', 'b', 'e']
        updated_locs = [0, 1, 2, 3]

        unit = cat.UnitData(data)
        assert list(unit._mapping.keys()) == data
        assert list(unit._mapping.values()) == locs

        unit.update(data_update)
        assert list(unit._mapping.keys()) == unique_data
        assert list(unit._mapping.values()) == updated_locs
