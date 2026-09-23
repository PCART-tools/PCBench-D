    def getprojection(self) -> tuple[list[int], list[int]]:
        """
        Get projection to x and y axes

        :returns: Two sequences, indicating where there are non-zero
            pixels along the X-axis and the Y-axis, respectively.
        """

        self.load()
        x, y = self.im.getprojection()
        return list(x), list(y)
