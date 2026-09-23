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
