    def delete(self, loc):
        new_left = self.left.delete(loc)
        new_right = self.right.delete(loc)
        return self._shallow_copy(new_left, new_right)
