        def set_pixmap (self, pixmap):
            self.gc.ctx = cairo.gtk.gdk_cairo_create (pixmap)
