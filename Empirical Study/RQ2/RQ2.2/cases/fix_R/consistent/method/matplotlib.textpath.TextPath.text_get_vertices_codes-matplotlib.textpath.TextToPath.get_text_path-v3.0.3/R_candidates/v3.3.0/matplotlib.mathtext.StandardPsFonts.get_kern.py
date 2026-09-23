    def get_kern(self, font1, fontclass1, sym1, fontsize1,
                 font2, fontclass2, sym2, fontsize2, dpi):
        if font1 == font2 and fontsize1 == fontsize2:
            info1 = self._get_info(font1, fontclass1, sym1, fontsize1, dpi)
            info2 = self._get_info(font2, fontclass2, sym2, fontsize2, dpi)
            font = info1.font
            return (font.get_kern_dist(info1.glyph, info2.glyph)
                    * 0.001 * fontsize1)
        return Fonts.get_kern(self, font1, fontclass1, sym1, fontsize1,
                              font2, fontclass2, sym2, fontsize2, dpi)
