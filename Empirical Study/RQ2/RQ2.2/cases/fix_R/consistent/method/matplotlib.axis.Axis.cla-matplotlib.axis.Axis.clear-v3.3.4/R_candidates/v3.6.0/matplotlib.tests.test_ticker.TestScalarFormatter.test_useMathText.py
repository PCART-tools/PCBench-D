    @pytest.mark.parametrize('use_math_text', useMathText_data)
    def test_useMathText(self, use_math_text):
        with mpl.rc_context({'axes.formatter.use_mathtext': use_math_text}):
            tmp_form = mticker.ScalarFormatter()
            assert use_math_text == tmp_form.get_useMathText()
