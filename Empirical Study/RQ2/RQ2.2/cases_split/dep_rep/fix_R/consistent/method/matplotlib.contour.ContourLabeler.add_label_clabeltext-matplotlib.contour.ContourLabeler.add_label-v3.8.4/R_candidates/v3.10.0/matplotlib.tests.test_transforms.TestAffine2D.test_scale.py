    def test_scale(self):
        sx = Affine2D().scale(3, 1)
        sy = Affine2D().scale(1, -2)
        trans = Affine2D().scale(3, -2)
        assert_array_equal((sx + sy).get_matrix(), trans.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [3, -2])
        assert_array_equal(trans.transform(self.multiple_points),
                           [[0, -4], [9, -6], [12, 0]])
