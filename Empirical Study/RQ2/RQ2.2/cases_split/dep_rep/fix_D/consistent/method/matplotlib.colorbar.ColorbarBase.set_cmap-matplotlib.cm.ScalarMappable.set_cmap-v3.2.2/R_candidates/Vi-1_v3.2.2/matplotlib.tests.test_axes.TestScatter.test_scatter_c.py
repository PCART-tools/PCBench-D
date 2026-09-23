    @pytest.mark.parametrize('c_case, re_key', params_test_scatter_c)
    def test_scatter_c(self, c_case, re_key):
        def get_next_color():
            return 'blue'  # currently unused

        from matplotlib.axes import Axes

        xsize = 4

        # Additional checking of *c* (introduced in #11383).
        REGEXP = {
            "shape": "^'c' argument has [0-9]+ elements",  # shape mismatch
            "conversion": "^'c' argument must be a color",  # bad vals
            }

        if re_key is None:
            Axes._parse_scatter_color_args(
                c=c_case, edgecolors="black", kwargs={}, xsize=xsize,
                get_next_color_func=get_next_color)
        else:
            with pytest.raises(ValueError, match=REGEXP[re_key]):
                Axes._parse_scatter_color_args(
                    c=c_case, edgecolors="black", kwargs={}, xsize=xsize,
                    get_next_color_func=get_next_color)
