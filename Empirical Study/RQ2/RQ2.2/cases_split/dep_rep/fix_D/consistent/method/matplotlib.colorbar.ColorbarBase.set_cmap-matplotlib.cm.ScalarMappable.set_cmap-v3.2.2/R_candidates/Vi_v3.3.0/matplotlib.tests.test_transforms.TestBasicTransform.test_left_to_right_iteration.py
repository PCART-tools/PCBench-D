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
