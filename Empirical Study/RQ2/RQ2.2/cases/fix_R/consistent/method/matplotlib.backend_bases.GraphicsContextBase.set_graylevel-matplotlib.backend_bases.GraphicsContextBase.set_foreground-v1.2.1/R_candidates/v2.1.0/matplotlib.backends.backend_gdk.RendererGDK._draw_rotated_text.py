    def _draw_rotated_text(self, gc, x, y, s, prop, angle):
        """
        Draw the text rotated 90 degrees, other angles are not supported
        """
        # this function (and its called functions) is a bottleneck
        # Pango 1.6 supports rotated text, but pygtk 2.4.0 does not yet have
        # wrapper functions
        # GTK+ 2.6 pixbufs support rotation

        gdrawable = self.gdkDrawable
        ggc = gc.gdkGC

        layout, inkRect, logicalRect = self._get_pango_layout(s, prop)
        l, b, w, h = inkRect
        x = int(x-h)
        y = int(y-w)

        if (x < 0 or y < 0 or # window has shrunk and text is off the edge
            x + w > self.width or y + h > self.height):
            return

        key = (x,y,s,angle,hash(prop))
        imageVert = self.rotated.get(key)
        if imageVert != None:
            gdrawable.draw_image(ggc, imageVert, 0, 0, x, y, h, w)
            return

        imageBack = gdrawable.get_image(x, y, w, h)
        imageVert = gdrawable.get_image(x, y, h, w)
        imageFlip = gtk.gdk.Image(type=gdk.IMAGE_FASTEST,
                                  visual=gdrawable.get_visual(),
                                  width=w, height=h)
        if imageFlip == None or imageBack == None or imageVert == None:
            warnings.warn("Could not renderer vertical text")
            return
        imageFlip.set_colormap(self._cmap)
        for i in range(w):
            for j in range(h):
                imageFlip.put_pixel(i, j, imageVert.get_pixel(j,w-i-1) )

        gdrawable.draw_image(ggc, imageFlip, 0, 0, x, y, w, h)
        gdrawable.draw_layout(ggc, x, y-b, layout)

        imageIn  = gdrawable.get_image(x, y, w, h)
        for i in range(w):
            for j in range(h):
                imageVert.put_pixel(j, i, imageIn.get_pixel(w-i-1,j) )

        gdrawable.draw_image(ggc, imageBack, 0, 0, x, y, w, h)
        gdrawable.draw_image(ggc, imageVert, 0, 0, x, y, h, w)
        self.rotated[key] = imageVert
