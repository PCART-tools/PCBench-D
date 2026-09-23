    @pytest.fixture
    def missing_data(self):
        self.dm = ['here', np.nan, 'here', 'there']
        self.dmticks = [0, -1, 1]
        self.dmlabels = ['here', 'nan', 'there']
        unitmap = [('here', 0), ('nan', -1), ('there', 1)]
        self.dmunit_data = MockUnitData(unitmap)
