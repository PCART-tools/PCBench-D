    @pytest.mark.parametrize("data, unitmap, exp", testdata, ids=ids)
    def test_convert(self, data, unitmap, exp):
        MUD = MockUnitData(unitmap)
        axis = FakeAxis(MUD)
        act = self.cc.convert(data, None, axis)
        np.testing.assert_array_equal(act, exp)
