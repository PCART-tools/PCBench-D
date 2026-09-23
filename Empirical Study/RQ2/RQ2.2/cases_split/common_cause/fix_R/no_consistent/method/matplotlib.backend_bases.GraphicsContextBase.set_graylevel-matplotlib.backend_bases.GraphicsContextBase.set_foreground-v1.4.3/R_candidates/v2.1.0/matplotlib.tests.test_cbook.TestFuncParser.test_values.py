    @pytest.mark.parametrize("string, func",
                             zip(validstrings, results),
                             ids=validstrings)
    def test_values(self, string, func):
        func_parser = cbook._StringFuncParser(string)
        f = func_parser.function
        assert_array_almost_equal(f(self.x_test), func(self.x_test))
