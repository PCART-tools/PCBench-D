class TestBasicTransform:
    def setup_method(self):

        self.ta1 = mtransforms.Affine2D(shorthand_name='ta1').rotate(np.pi / 2)
        self.ta2 = mtransforms.Affine2D(shorthand_name='ta2').translate(10, 0)
        self.ta3 = mtransforms.Affine2D(shorthand_name='ta3').scale(1, 2)

        self.tn1 = NonAffineForTest(mtransforms.Affine2D().translate(1, 2),
                                    shorthand_name='tn1')
        self.tn2 = NonAffineForTest(mtransforms.Affine2D().translate(1, 2),
                                    shorthand_name='tn2')
        self.tn3 = NonAffineForTest(mtransforms.Affine2D().translate(1, 2),
                                    shorthand_name='tn3')

        # creates a transform stack which looks like ((A, (N, A)), A)
        self.stack1 = (self.ta1 + (self.tn1 + self.ta2)) + self.ta3
        # creates a transform stack which looks like (((A, N), A), A)
        self.stack2 = self.ta1 + self.tn1 + self.ta2 + self.ta3
        # creates a transform stack which is a subset of stack2
        self.stack2_subset = self.tn1 + self.ta2 + self.ta3

        # when in debug, the transform stacks can produce dot images:
#        self.stack1.write_graphviz(file('stack1.dot', 'w'))
#        self.stack2.write_graphviz(file('stack2.dot', 'w'))
#        self.stack2_subset.write_graphviz(file('stack2_subset.dot', 'w'))

    def test_transform_depth(self):
        assert self.stack1.depth == 4
        assert self.stack2.depth == 4
        assert self.stack2_subset.depth == 3

    def test_left_to_right_iteration(self):
        stack3 = (self.ta1 + (self.tn1 + (self.ta2 + self.tn2))) + self.ta3
#        stack3.write_graphviz(file('stack3.dot', 'w'))

        target_transforms = [stack3,
                             (self.tn1 + (self.ta2 + self.tn2)) + self.ta3,
                             (self.ta2 + self.tn2) + self.ta3,
                             self.tn2 + self.ta3,
                             self.ta3,
                             ]
        r = [rh for _, rh in stack3._iter_break_from_left_to_right()]
        assert len(r) == len(target_transforms)

        for target_stack, stack in zip(target_transforms, r):
            assert target_stack == stack

    def test_transform_shortcuts(self):
        assert self.stack1 - self.stack2_subset == self.ta1
        assert self.stack2 - self.stack2_subset == self.ta1

        assert self.stack2_subset - self.stack2 == self.ta1.inverted()
        assert (self.stack2_subset - self.stack2).depth == 1

        with pytest.raises(ValueError):
            self.stack1 - self.stack2

        aff1 = self.ta1 + (self.ta2 + self.ta3)
        aff2 = self.ta2 + self.ta3

        assert aff1 - aff2 == self.ta1
        assert aff1 - self.ta2 == aff1 + self.ta2.inverted()

        assert self.stack1 - self.ta3 == self.ta1 + (self.tn1 + self.ta2)
        assert self.stack2 - self.ta3 == self.ta1 + self.tn1 + self.ta2

        assert ((self.ta2 + self.ta3) - self.ta3 + self.ta3 ==
                self.ta2 + self.ta3)

    def test_contains_branch(self):
        r1 = (self.ta2 + self.ta1)
        r2 = (self.ta2 + self.ta1)
        assert r1 == r2
        assert r1 != self.ta1
        assert r1.contains_branch(r2)
        assert r1.contains_branch(self.ta1)
        assert not r1.contains_branch(self.ta2)
        assert not r1.contains_branch(self.ta2 + self.ta2)

        assert r1 == r2

        assert self.stack1.contains_branch(self.ta3)
        assert self.stack2.contains_branch(self.ta3)

        assert self.stack1.contains_branch(self.stack2_subset)
        assert self.stack2.contains_branch(self.stack2_subset)

        assert not self.stack2_subset.contains_branch(self.stack1)
        assert not self.stack2_subset.contains_branch(self.stack2)

        assert self.stack1.contains_branch(self.ta2 + self.ta3)
        assert self.stack2.contains_branch(self.ta2 + self.ta3)

        assert not self.stack1.contains_branch(self.tn1 + self.ta2)

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
