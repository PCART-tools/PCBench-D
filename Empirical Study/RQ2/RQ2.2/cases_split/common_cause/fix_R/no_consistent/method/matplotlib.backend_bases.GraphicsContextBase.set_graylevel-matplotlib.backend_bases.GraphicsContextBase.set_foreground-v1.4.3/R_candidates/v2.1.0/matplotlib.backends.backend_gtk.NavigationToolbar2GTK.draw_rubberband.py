    def draw_rubberband(self, event, x0, y0, x1, y1):
        'adapted from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189744'
        drawable = self.canvas.window
        if drawable is None:
            return

        gc = drawable.new_gc()

        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0

        w = abs(x1 - x0)
        h = abs(y1 - y0)

        rect = [int(val)for val in (min(x0,x1), min(y0, y1), w, h)]
        try:
            lastrect, pixmapBack = self._pixmapBack
        except AttributeError:
            #snap image back
            if event.inaxes is None:
                return

            ax = event.inaxes
            l,b,w,h = [int(val) for val in ax.bbox.bounds]
            b = int(height)-(b+h)
            axrect = l,b,w,h
            self._pixmapBack = axrect, gtk.gdk.Pixmap(drawable, w, h)
            self._pixmapBack[1].draw_drawable(gc, drawable, l, b, 0, 0, w, h)
        else:
            drawable.draw_drawable(gc, pixmapBack, 0, 0, *lastrect)
        drawable.draw_rectangle(gc, False, *rect)
