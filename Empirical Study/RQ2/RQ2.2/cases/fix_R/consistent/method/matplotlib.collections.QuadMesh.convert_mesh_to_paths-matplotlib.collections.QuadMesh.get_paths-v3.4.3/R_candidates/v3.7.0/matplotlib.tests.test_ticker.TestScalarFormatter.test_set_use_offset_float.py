    def test_set_use_offset_float(self):
        tmp_form = mticker.ScalarFormatter()
        tmp_form.set_useOffset(0.5)
        assert not tmp_form.get_useOffset()
        assert tmp_form.offset == 0.5
