    @pytest.mark.parametrize('c_case, re_key', params_test_scatter_c)
    def test_scatter_c(self, c_case, re_key):
        # Additional checking of *c* (introduced in #11383).
        REGEXP = {
            "shape": "^'c' argument has [0-9]+ elements",  # shape mismatch
            "conversion": "^'c' argument must either be valid",  # bad vals
            }
        x = y = [0, 1, 2, 3]
        fig, ax = plt.subplots()

        if re_key is None:
            ax.scatter(x, y, c=c_case, edgecolors="black")
        else:
            with pytest.raises(ValueError, match=REGEXP[re_key]):
                ax.scatter(x, y, c=c_case, edgecolors="black")
