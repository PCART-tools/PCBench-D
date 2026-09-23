@_api.deprecated("3.6")
class _RendererGTKCairo(RendererCairo):
    def set_context(self, ctx):
        if (cairo.__name__ == "cairocffi"
                and not isinstance(ctx, cairo.Context)):
            ctx = cairo.Context._from_pointer(
                cairo.ffi.cast(
                    'cairo_t **',
                    id(ctx) + object.__basicsize__)[0],
                incref=True)
        self.gc.ctx = ctx
