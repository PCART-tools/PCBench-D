    @pytest.mark.parametrize('use_offset', use_offset_data)
    def test_use_offset(self, use_offset):
        with matplotlib.rc_context({'axes.formatter.useoffset': use_offset}):
            tmp_form = mticker.ScalarFormatter()
            assert use_offset == tmp_form.get_useOffset()
