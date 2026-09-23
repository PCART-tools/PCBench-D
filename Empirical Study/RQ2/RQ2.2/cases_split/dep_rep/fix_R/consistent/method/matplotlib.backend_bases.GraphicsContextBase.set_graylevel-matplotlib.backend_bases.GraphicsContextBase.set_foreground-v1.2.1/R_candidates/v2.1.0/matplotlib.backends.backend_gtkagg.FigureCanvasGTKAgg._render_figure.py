    def _render_figure(self, pixmap, width, height):
        if DEBUG: print('FigureCanvasGTKAgg.render_figure')
        FigureCanvasAgg.draw(self)
        if DEBUG: print('FigureCanvasGTKAgg.render_figure pixmap', pixmap)
        #agg_to_gtk_drawable(pixmap, self.renderer._renderer, None)

        buf = self.buffer_rgba()
        ren = self.get_renderer()
        w = int(ren.width)
        h = int(ren.height)

        pixbuf = gtk.gdk.pixbuf_new_from_data(
            buf, gtk.gdk.COLORSPACE_RGB,  True, 8, w, h, w*4)
        pixmap.draw_pixbuf(pixmap.new_gc(), pixbuf, 0, 0, 0, 0, w, h,
                           gtk.gdk.RGB_DITHER_NONE, 0, 0)
        if DEBUG: print('FigureCanvasGTKAgg.render_figure done')
