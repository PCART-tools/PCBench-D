    @pytest.mark.parametrize("string, bounded",
                             zip(validstrings, bounded_list),
                             ids=validstrings)
    def test_bounded(self, string, bounded):
        func_parser = cbook._StringFuncParser(string)
        b = func_parser.is_bounded_0_1
        assert_array_equal(b, bounded)
