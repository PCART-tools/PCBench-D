    def render_glyph(self, ox, oy, info):
        oy = self.height - oy + info.offset
        postscript_name = info.postscript_name
        fontsize        = info.fontsize
        symbol_name     = info.symbol_name

        if (postscript_name, fontsize) != self.lastfont:
            ps = """/%(postscript_name)s findfont
%(fontsize)s scalefont
setfont
""" % locals()
            self.lastfont = postscript_name, fontsize
            self.pswriter.write(ps)

        ps = """%(ox)f %(oy)f moveto
/%(symbol_name)s glyphshow\n
""" % locals()
        self.pswriter.write(ps)
