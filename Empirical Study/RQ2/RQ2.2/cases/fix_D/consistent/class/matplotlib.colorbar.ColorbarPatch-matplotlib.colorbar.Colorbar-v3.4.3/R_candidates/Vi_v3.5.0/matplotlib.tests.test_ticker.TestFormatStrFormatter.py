class TestFormatStrFormatter:
    def test_basic(self):
        # test % style formatter
        tmp_form = mticker.FormatStrFormatter('%05d')
        assert '00002' == tmp_form(2)
