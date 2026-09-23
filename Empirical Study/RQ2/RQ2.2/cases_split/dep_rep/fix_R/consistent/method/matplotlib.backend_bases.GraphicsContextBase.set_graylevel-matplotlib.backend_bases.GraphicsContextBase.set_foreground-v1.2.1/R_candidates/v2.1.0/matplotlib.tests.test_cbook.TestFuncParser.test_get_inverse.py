    @pytest.mark.parametrize("string", validstrings, ids=validstrings)
    def test_get_inverse(self, string):
        func_parser = cbook._StringFuncParser(string)
        finv1 = func_parser.inverse
        finv2 = func_parser.func_info.inverse
        assert_array_almost_equal(finv1(self.x_test), finv2(self.x_test))
