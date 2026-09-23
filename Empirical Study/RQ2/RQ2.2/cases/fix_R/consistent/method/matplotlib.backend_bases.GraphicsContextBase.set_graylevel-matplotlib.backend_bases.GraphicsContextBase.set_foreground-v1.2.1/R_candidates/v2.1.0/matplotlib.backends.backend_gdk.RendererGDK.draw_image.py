    def draw_image(self, gc, x, y, im):
        bbox = gc.get_clip_rectangle()

        if bbox != None:
            l,b,w,h = bbox.bounds
            #rectangle = (int(l), self.height-int(b+h),
            #             int(w), int(h))
            # set clip rect?

        rows, cols = im.shape[:2]

        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,
                                has_alpha=True, bits_per_sample=8,
                                width=cols, height=rows)

        array = pixbuf_get_pixels_array(pixbuf)
        array[:, :, :] = im[::-1]

        gc = self.new_gc()


        y = self.height-y-rows

        try: # new in 2.2
            # can use None instead of gc.gdkGC, if don't need clipping
            self.gdkDrawable.draw_pixbuf (gc.gdkGC, pixbuf, 0, 0,
                                          int(x), int(y), cols, rows,
                                          gdk.RGB_DITHER_NONE, 0, 0)
        except AttributeError:
            # deprecated in 2.2
            pixbuf.render_to_drawable(self.gdkDrawable, gc.gdkGC, 0, 0,
                                  int(x), int(y), cols, rows,
                                  gdk.RGB_DITHER_NONE, 0, 0)
