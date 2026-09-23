    def draw_image(self, gc, x, y, im):
        # bbox - not currently used
        if sys.byteorder == 'little':
            im = im[:, :, (2, 1, 0, 3)]
        else:
            im = im[:, :, (3, 0, 1, 2)]
        if HAS_CAIRO_CFFI:
            # cairocffi tries to use the buffer_info from array.array
            # that we replicate in ArrayWrapper and alternatively falls back
            # on ctypes to get a pointer to the numpy array. This works
            # correctly on a numpy array in python3 but not 2.7. We replicate
            # the array.array functionality here to get cross version support.
            imbuffer = ArrayWrapper(im.flatten())
        else:
            # py2cairo uses PyObject_AsWriteBuffer
            # to get a pointer to the numpy array this works correctly
            # on a regular numpy array but not on a memory view.
            # At the time of writing the latest release version of
            # py3cairo still does not support create_for_data
            imbuffer = im.flatten()
        surface = cairo.ImageSurface.create_for_data(
            imbuffer, cairo.FORMAT_ARGB32,
            im.shape[1], im.shape[0], im.shape[1]*4)
        ctx = gc.ctx
        y = self.height - y - im.shape[0]

        ctx.save()
        ctx.set_source_surface(surface, float(x), float(y))
        if gc.get_alpha() != 1.0:
            ctx.paint_with_alpha(gc.get_alpha())
        else:
            ctx.paint()
        ctx.restore()
