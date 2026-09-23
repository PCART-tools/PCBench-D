    def set_font(self, fontname, fontsize, store=True):
        if mpl.rcParams['ps.useafm']:
            return
        if (fontname, fontsize) != (self.fontname, self.fontsize):
            out = ("/%s findfont\n"
                   "%1.3f scalefont\n"
                   "setfont\n" % (fontname, fontsize))
            self._pswriter.write(out)
            if store:
                self.fontname = fontname
                self.fontsize = fontsize
