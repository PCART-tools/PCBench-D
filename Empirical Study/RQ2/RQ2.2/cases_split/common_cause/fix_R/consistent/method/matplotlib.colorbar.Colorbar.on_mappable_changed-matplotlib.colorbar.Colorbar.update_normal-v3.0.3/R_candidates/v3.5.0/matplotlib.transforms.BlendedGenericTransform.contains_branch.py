    def contains_branch(self, other):
        # A blended transform cannot possibly contain a branch from two
        # different transforms.
        return False
