    def contains_branch_seperately(self, transform):
        # Note, this is an exact copy of BlendedAffine2D.contains_branch_seperately
        return self._x.contains_branch(transform), self._y.contains_branch(transform)
