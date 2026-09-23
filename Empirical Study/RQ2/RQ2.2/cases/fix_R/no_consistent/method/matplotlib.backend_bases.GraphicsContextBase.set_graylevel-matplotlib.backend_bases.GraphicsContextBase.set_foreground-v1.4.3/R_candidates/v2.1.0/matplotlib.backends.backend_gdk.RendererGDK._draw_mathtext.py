    def _draw_mathtext(self, gc, x, y, s, prop, angle):
        ox, oy, width, height, descent, font_image, used_characters = \
            self.mathtext_parser.parse(s, self.dpi, prop)

        if angle == 90:
            width, height = height, width
            x -= width
        y -= height

        imw = font_image.get_width()
        imh = font_image.get_height()

        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, has_alpha=True,
                                bits_per_sample=8, width=imw, height=imh)

        array = pixbuf_get_pixels_array(pixbuf)

        rgb = gc.get_rgb()
        array[:,:,0] = int(rgb[0]*255)
        array[:,:,1] = int(rgb[1]*255)
        array[:,:,2] = int(rgb[2]*255)
        array[:,:,3] = (
            np.fromstring(font_image.as_str(), np.uint8).reshape((imh, imw)))

        # can use None instead of gc.gdkGC, if don't need clipping
        self.gdkDrawable.draw_pixbuf(gc.gdkGC, pixbuf, 0, 0,
                                     int(x), int(y), imw, imh,
                                     gdk.RGB_DITHER_NONE, 0, 0)
