    def test_skew(self):
        trans_rad = Affine2D().skew(np.pi / 8, np.pi / 12)
        trans_deg = Affine2D().skew_deg(22.5, 15)
        assert_array_equal(trans_rad.get_matrix(), trans_deg.get_matrix())
        # Using ~atan(0.5), ~atan(0.25) produces roundish numbers on output.
        trans = Affine2D().skew_deg(26.5650512, 14.0362435)
        assert_array_almost_equal(trans.transform(self.single_point), [1.5, 1.25])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[1, 2], [4.5, 3.75], [4, 1]])
