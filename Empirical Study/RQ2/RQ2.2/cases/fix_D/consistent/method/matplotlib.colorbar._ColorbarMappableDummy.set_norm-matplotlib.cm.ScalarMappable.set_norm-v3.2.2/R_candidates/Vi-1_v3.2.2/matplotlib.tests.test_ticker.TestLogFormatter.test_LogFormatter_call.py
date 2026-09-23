    @pytest.mark.parametrize('val', [1, 10, 100, 1000])
    def test_LogFormatter_call(self, val):
        # test _num_to_string method used in __call__
        temp_lf = mticker.LogFormatter()
        temp_lf.axis = FakeAxis()
        assert temp_lf(val) == str(val)
