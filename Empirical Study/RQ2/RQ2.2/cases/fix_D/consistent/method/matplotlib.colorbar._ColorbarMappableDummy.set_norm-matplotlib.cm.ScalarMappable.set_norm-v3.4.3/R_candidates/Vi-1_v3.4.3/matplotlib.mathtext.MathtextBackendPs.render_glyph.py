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
