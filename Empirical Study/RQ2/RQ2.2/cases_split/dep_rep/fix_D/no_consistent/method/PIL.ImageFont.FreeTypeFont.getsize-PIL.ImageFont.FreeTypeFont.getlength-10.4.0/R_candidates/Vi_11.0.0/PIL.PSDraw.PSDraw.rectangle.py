    def rectangle(self, box: tuple[int, int, int, int]) -> None:
        """
        Draws a rectangle.

        :param box: A tuple of four integers, specifying left, bottom, width and
           height.
        """
        self.fp.write(b"%d %d M 0 %d %d Vr\n" % box)
