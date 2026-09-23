    def image(self, box, im, dpi=None):
        """Draw a PIL image, centered in the given box."""
        # default resolution depends on mode
        if not dpi:
            if im.mode == "1":
                dpi = 200  # fax
            else:
                dpi = 100  # greyscale
        # image size (on paper)
        x = im.size[0] * 72 / dpi
        y = im.size[1] * 72 / dpi
        # max allowed size
        xmax = float(box[2] - box[0])
        ymax = float(box[3] - box[1])
        if x > xmax:
            y = y * xmax / x
            x = xmax
        if y > ymax:
            x = x * ymax / y
            y = ymax
        dx = (xmax - x) / 2 + box[0]
        dy = (ymax - y) / 2 + box[1]
        self.fp.write(b"gsave\n%f %f translate\n" % (dx, dy))
        if (x, y) != im.size:
            # EpsImagePlugin._save prints the image at (0,0,xsize,ysize)
            sx = x / im.size[0]
            sy = y / im.size[1]
            self.fp.write(b"%f %f scale\n" % (sx, sy))
        EpsImagePlugin._save(im, self.fp, None, 0)
        self.fp.write(b"\ngrestore\n")
