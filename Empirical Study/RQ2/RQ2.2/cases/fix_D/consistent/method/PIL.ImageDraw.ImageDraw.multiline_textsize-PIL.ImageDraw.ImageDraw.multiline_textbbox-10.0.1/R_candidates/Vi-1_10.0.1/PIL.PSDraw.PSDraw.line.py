    def line(self, xy0, xy1):
        """
        Draws a line between the two points. Coordinates are given in
        PostScript point coordinates (72 points per inch, (0, 0) is the lower
        left corner of the page).
        """
        self.fp.write(b"%d %d %d %d Vl\n" % (*xy0, *xy1))
