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
