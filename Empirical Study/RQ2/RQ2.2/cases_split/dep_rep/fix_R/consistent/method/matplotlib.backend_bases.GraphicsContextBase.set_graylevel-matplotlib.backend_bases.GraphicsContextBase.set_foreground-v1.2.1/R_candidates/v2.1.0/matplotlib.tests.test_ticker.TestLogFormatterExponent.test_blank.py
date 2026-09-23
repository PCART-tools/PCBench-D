    def test_blank(self):
        # Should be a blank string for non-integer powers if labelOnlyBase=True
        formatter = mticker.LogFormatterExponent(base=10, labelOnlyBase=True)
        formatter.axis = FakeAxis()
        assert formatter(10**0.1) == ''
