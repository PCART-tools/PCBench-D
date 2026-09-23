    def test_affine_simplification(self):
        # tests that a transform stack only calls as much is absolutely
        # necessary "non-affine" allowing the best possible optimization with
        # complex transformation stacks.
        points = np.array([[0, 0], [10, 20], [np.nan, 1], [-1, 0]],
                          dtype=np.float64)
        na_pts = self.stack1.transform_non_affine(points)
        all_pts = self.stack1.transform(points)

        na_expected = np.array([[1., 2.], [-19., 12.],
                                [np.nan, np.nan], [1., 1.]], dtype=np.float64)
        all_expected = np.array([[11., 4.], [-9., 24.],
                                 [np.nan, np.nan], [11., 2.]],
                                dtype=np.float64)

        # check we have the expected results from doing the affine part only
        assert_array_almost_equal(na_pts, na_expected)
        # check we have the expected results from a full transformation
        assert_array_almost_equal(all_pts, all_expected)
        # check we have the expected results from doing the transformation in
        # two steps
        assert_array_almost_equal(self.stack1.transform_affine(na_pts),
                                  all_expected)
        # check that getting the affine transformation first, then fully
        # transforming using that yields the same result as before.
        assert_array_almost_equal(self.stack1.get_affine().transform(na_pts),
                                  all_expected)

        # check that the affine part of stack1 & stack2 are equivalent
        # (i.e. the optimization is working)
        expected_result = (self.ta2 + self.ta3).get_matrix()
        result = self.stack1.get_affine().get_matrix()
        assert_array_equal(expected_result, result)

        result = self.stack2.get_affine().get_matrix()
        assert_array_equal(expected_result, result)
