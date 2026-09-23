    @pytest.fixture
    def data(self):
        self.d = ['a', 'b', 'c', 'a']
        self.dticks = [0, 1, 2]
        self.dlabels = ['a', 'b', 'c']
        unitmap = [('a', 0), ('b', 1), ('c', 2)]
        self.dunit_data = MockUnitData(unitmap)
