    def set_context(self, ctx):
        if HAS_CAIRO_CFFI:
            ctx = cairo.Context._from_pointer(
                cairo.ffi.cast(
                    'cairo_t **',
                    id(ctx) + object.__basicsize__)[0],
                incref=True)

        self.gc.ctx = ctx
