    def test_transform_depth(self):
        assert self.stack1.depth == 4
        assert self.stack2.depth == 4
        assert self.stack2_subset.depth == 3
