    def test_translate(self):
        tx = Affine2D().translate(23, 0)
        ty = Affine2D().translate(0, 42)
        trans = Affine2D().translate(23, 42)
        assert_array_equal((tx + ty).get_matrix(), trans.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [24, 43])
        assert_array_equal(trans.transform(self.multiple_points),
                           [[23, 44], [26, 45], [27, 42]])
