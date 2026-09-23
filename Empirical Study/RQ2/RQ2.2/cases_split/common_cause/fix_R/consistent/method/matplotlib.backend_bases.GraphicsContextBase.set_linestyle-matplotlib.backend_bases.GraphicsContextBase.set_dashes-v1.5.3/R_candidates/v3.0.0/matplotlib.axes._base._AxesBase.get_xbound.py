    def get_xbound(self):
        """Return the lower and upper x-axis bounds, in increasing order."""
        left, right = self.get_xlim()
        if left < right:
            return left, right
        else:
            return right, left
