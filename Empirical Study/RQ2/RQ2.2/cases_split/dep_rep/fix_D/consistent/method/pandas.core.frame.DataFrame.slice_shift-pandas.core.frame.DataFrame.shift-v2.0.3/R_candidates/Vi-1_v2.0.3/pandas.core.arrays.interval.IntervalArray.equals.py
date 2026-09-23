    def equals(self, other) -> bool:
        if type(self) != type(other):
            return False

        return bool(
            self.closed == other.closed
            and self.left.equals(other.left)
            and self.right.equals(other.right)
        )
