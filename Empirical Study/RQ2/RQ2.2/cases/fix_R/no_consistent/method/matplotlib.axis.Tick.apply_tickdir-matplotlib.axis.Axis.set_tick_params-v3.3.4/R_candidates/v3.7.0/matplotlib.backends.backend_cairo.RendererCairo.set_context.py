    def set_context(self, ctx):
        surface = ctx.get_target()
        if hasattr(surface, "get_width") and hasattr(surface, "get_height"):
            size = surface.get_width(), surface.get_height()
        elif hasattr(surface, "get_extents"):  # GTK4 RecordingSurface.
            ext = surface.get_extents()
            size = ext.width, ext.height
        else:  # vector surfaces.
            ctx.save()
            ctx.reset_clip()
            rect, *rest = ctx.copy_clip_rectangle_list()
            if rest:
                raise TypeError("Cannot infer surface size")
            size = rect.width, rect.height
            ctx.restore()
        self.gc.ctx = ctx
        self.width, self.height = size
