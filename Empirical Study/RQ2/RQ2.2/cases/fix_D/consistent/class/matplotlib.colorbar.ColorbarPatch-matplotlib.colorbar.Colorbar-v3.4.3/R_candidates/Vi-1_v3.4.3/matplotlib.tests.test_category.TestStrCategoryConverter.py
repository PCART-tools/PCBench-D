class TestStrCategoryConverter:
    """
    Based on the pandas conversion and factorization tests:

    ref: /pandas/tseries/tests/test_converter.py
         /pandas/tests/test_algos.py:TestFactorize
    """
    test_cases = [("unicode", ["Здравствуйте мир"]),
                  ("ascii", ["hello world"]),
                  ("single", ['a', 'b', 'c']),
                  ("integer string", ["1", "2"]),
                  ("single + values>10", ["A", "B", "C", "D", "E", "F", "G",
                                          "H", "I", "J", "K", "L", "M", "N",
                                          "O", "P", "Q", "R", "S", "T", "U",
                                          "V", "W", "X", "Y", "Z"])]

    ids, values = zip(*test_cases)

    failing_test_cases = [("mixed", [3.14, 'A', np.inf]),
                          ("string integer", ['42', 42])]

    fids, fvalues = zip(*failing_test_cases)

    @pytest.fixture(autouse=True)
    def mock_axis(self, request):
        self.cc = cat.StrCategoryConverter()
        # self.unit should be probably be replaced with real mock unit
        self.unit = cat.UnitData()
        self.ax = FakeAxis(self.unit)

    @pytest.mark.parametrize("vals", values, ids=ids)
    def test_convert(self, vals):
        np.testing.assert_allclose(self.cc.convert(vals, self.ax.units,
                                                   self.ax),
                                   range(len(vals)))

    @pytest.mark.parametrize("value", ["hi", "мир"], ids=["ascii", "unicode"])
    def test_convert_one_string(self, value):
        assert self.cc.convert(value, self.unit, self.ax) == 0

    def test_convert_one_number(self):
        actual = self.cc.convert(0.0, self.unit, self.ax)
        np.testing.assert_allclose(actual, np.array([0.]))

    def test_convert_float_array(self):
        data = np.array([1, 2, 3], dtype=float)
        actual = self.cc.convert(data, self.unit, self.ax)
        np.testing.assert_allclose(actual, np.array([1., 2., 3.]))

    @pytest.mark.parametrize("fvals", fvalues, ids=fids)
    def test_convert_fail(self, fvals):
        with pytest.raises(TypeError):
            self.cc.convert(fvals, self.unit, self.ax)

    def test_axisinfo(self):
        axis = self.cc.axisinfo(self.unit, self.ax)
        assert isinstance(axis.majloc, cat.StrCategoryLocator)
        assert isinstance(axis.majfmt, cat.StrCategoryFormatter)

    def test_default_units(self):
        assert isinstance(self.cc.default_units(["a"], self.ax), cat.UnitData)
