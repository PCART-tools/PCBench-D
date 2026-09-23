    @pytest.mark.parametrize(
        "x,match",
        [
            (
                [["A", "."], [".", "A"]],
                (
                    "(?m)we found that the label .A. specifies a "
                    + "non-rectangular or non-contiguous area."
                ),
            ),
            (
                [["A", "B"], [None, [["A", "B"], ["C", "D"]]]],
                "There are duplicate keys .* between the outer layout",
            ),
            ("AAA\nc\nBBB", "All of the rows must be the same length"),
            (
                [["A", [["B", "C"], ["D"]]], ["E", "E"]],
                "All of the rows must be the same length",
            ),
        ],
    )
    def test_fail(self, x, match):
        fig = plt.figure()
        with pytest.raises(ValueError, match=match):
            fig.subplot_mosaic(x)
