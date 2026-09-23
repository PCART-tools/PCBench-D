    def _getextrema(self):
        """Get min/max values for each band in the image"""

        def minmax(histogram):
            n = 255
            x = 0
            for i in range(256):
                if histogram[i]:
                    n = min(n, i)
                    x = max(x, i)
            return n, x  # returns (255, 0) if there's no data in the histogram

        v = []
        for i in range(0, len(self.h), 256):
            v.append(minmax(self.h[i:]))
        return v
