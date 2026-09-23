    def _getextrema(self):
        """Get min/max values for each band in the image"""

        def minmax(histogram):
            res_min, res_max = 255, 0
            for i in range(256):
                if histogram[i]:
                    res_min = i
                    break
            for i in range(255, -1, -1):
                if histogram[i]:
                    res_max = i
                    break
            return res_min, res_max

        return [minmax(self.h[i:]) for i in range(0, len(self.h), 256)]
