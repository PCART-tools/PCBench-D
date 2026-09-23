    @pytest.mark.parametrize('c_case, re_key', params_test_scatter_c)
    def test_scatter_c(self, c_case, re_key):
        def get_next_color():
            return 'blue'  # currently unused

        xsize = 4
        # Additional checking of *c* (introduced in #11383).
        REGEXP = {
            "shape": "^'c' argument has [0-9]+ elements",  # shape mismatch
            "conversion": "^'c' argument must be a color",  # bad vals
            }

        assert_context = (
            pytest.raises(ValueError, match=REGEXP[re_key])
            if re_key is not None
            else pytest.warns(match="argument looks like a single numeric RGB")
            if isinstance(c_case, list) and len(c_case) == 3
            else contextlib.nullcontext()
        )
        with assert_context:
            mpl.axes.Axes._parse_scatter_color_args(
                c=c_case, edgecolors="black", kwargs={}, xsize=xsize,
                get_next_color_func=get_next_color)
