    def _getcount(self):
        """Get total number of pixels in each layer"""

        v = []
        for i in range(0, len(self.h), 256):
            v.append(functools.reduce(operator.add, self.h[i : i + 256]))
        return v
