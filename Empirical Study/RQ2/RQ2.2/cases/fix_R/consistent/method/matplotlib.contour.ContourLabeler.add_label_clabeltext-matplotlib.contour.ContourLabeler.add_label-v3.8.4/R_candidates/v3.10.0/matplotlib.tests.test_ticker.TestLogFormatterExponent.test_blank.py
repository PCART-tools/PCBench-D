    def test_blank(self):
        # Should be a blank string for non-integer powers if labelOnlyBase=True
        formatter = mticker.LogFormatterExponent(base=10, labelOnlyBase=True)
        formatter.create_dummy_axis()
        formatter.axis.set_view_interval(1, 10)
        assert formatter(10**0.1) == ''
