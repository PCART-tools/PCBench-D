@_api.deprecated("3.4", alternative="MathtextBackendPath")
class MathtextBackendPs(MathtextBackend):
    """
    Store information to write a mathtext rendering to the PostScript backend.
    """

    _PSResult = namedtuple(
        "_PSResult", "width height depth pswriter used_characters")

    def __init__(self):
        self.pswriter = StringIO()
        self.lastfont = None

    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset
        postscript_name = info.postscript_name
        fontsize = info.fontsize

        if (postscript_name, fontsize) != self.lastfont:
            self.lastfont = postscript_name, fontsize
            self.pswriter.write(
                f"/{postscript_name} findfont\n"
                f"{fontsize} scalefont\n"
                f"setfont\n")

        self.pswriter.write(
            f"{ox:f} {oy:f} moveto\n"
            f"/{info.symbol_name} glyphshow\n")

    def render_rect_filled(self, x1, y1, x2, y2):
        ps = "%f %f %f %f rectfill\n" % (
            x1, self.height - y2, x2 - x1, y2 - y1)
        self.pswriter.write(ps)

    def get_results(self, box, used_characters):
        _mathtext.ship(0, 0, box)
        return self._PSResult(self.width,
                              self.height + self.depth,
                              self.depth,
                              self.pswriter,
                              used_characters)
