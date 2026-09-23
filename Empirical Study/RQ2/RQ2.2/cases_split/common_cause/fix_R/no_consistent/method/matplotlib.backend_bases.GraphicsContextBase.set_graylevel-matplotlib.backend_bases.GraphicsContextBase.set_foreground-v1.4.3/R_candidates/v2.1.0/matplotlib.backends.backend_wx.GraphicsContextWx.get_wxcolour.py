    def get_wxcolour(self, color):
        """return a wx.Colour from RGB format"""
        DEBUG_MSG("get_wx_color()", 1, self)
        if len(color) == 3:
            r, g, b = color
            r *= 255
            g *= 255
            b *= 255
            return wx.Colour(red=int(r), green=int(g), blue=int(b))
        else:
            r, g, b, a = color
            r *= 255
            g *= 255
            b *= 255
            a *= 255
            return wx.Colour(
                red=int(r),
                green=int(g),
                blue=int(b),
                alpha=int(a))
