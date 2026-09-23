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

        blend = mtransforms.BlendedGenericTransform(self.tn2, self.stack2)
        x, y = blend.contains_branch_seperately(self.stack2_subset)
        stack_blend = self.tn3 + blend
        sx, sy = stack_blend.contains_branch_seperately(self.stack2_subset)
        assert x is sx is False
        assert y is sy is True
