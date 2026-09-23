    def contains_branch_seperately(self, transform):
        return (self._x.contains_branch(transform),
                self._y.contains_branch(transform))
