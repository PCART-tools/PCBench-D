    @pytest.mark.parametrize("string", validstrings, ids=validstrings)
    def test_inverse(self, string):
        func_parser = cbook._StringFuncParser(string)
        f = func_parser.func_info
        fdir = f.function
        finv = f.inverse
        assert_array_almost_equal(finv(fdir(self.x_test)), self.x_test)
