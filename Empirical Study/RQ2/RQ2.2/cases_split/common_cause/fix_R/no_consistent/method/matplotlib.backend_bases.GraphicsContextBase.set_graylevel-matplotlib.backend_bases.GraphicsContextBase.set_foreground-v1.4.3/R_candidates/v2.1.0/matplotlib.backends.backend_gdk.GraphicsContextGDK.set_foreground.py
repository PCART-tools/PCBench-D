    def set_foreground(self, fg, isRGBA=False):
        GraphicsContextBase.set_foreground(self, fg, isRGBA)
        self.gdkGC.foreground = self.rgb_to_gdk_color(self.get_rgb())
