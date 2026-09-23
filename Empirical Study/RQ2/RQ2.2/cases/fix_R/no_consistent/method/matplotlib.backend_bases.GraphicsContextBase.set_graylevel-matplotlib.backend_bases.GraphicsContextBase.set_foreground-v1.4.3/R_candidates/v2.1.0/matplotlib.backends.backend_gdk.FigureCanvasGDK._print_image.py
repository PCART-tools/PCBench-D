    def _print_image(self, filename, format, *args, **kwargs):
        width, height = self.get_width_height()
        pixmap = gtk.gdk.Pixmap (None, width, height, depth=24)
        self._render_figure(pixmap, width, height)

        # jpg colors don't match the display very well, png colors match
        # better
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, 0, 8,
                                width, height)
        pixbuf.get_from_drawable(pixmap, pixmap.get_colormap(),
                                 0, 0, 0, 0, width, height)

        # set the default quality, if we are writing a JPEG.
        # http://www.pygtk.org/docs/pygtk/class-gdkpixbuf.html#method-gdkpixbuf--save
        options = {k: kwargs[k] for k in ['quality'] if k in kwargs}
        if format in ['jpg', 'jpeg']:
            options.setdefault('quality', rcParams['savefig.jpeg_quality'])
            options['quality'] = str(options['quality'])

        pixbuf.save(filename, format, options=options)
