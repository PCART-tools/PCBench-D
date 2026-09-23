    @pytest.fixture(autouse=True)
    def mock_axis(self, request):
        self.cc = cat.StrCategoryConverter()
        # self.unit should be probably be replaced with real mock unit
        self.unit = cat.UnitData()
        self.ax = FakeAxis(self.unit)
