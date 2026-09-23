    def set_font(self, fontname, fontsize, store=True):
        if (fontname, fontsize) != (self.fontname, self.fontsize):
            self._pswriter.write(f"/{fontname} {fontsize:1.3f} selectfont\n")
            if store:
                self.fontname = fontname
                self.fontsize = fontsize
