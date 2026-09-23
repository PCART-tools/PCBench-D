    def set_dashes(self, dash_offset, dash_list):
        GraphicsContextBase.set_dashes(self, dash_offset, dash_list)

        if dash_list == None:
            self.gdkGC.line_style = gdk.LINE_SOLID
        else:
            pixels = self.renderer.points_to_pixels(np.asarray(dash_list))
            dl = [max(1, int(np.round(val))) for val in pixels]
            self.gdkGC.set_dashes(dash_offset, dl)
            self.gdkGC.line_style = gdk.LINE_ON_OFF_DASH
