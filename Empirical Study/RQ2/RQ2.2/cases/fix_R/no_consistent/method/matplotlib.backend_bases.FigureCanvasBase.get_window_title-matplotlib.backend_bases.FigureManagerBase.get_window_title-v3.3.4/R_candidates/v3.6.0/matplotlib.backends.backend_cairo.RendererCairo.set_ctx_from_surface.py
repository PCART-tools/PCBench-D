    @_api.deprecated("3.6", alternative="set_context")
    def set_ctx_from_surface(self, surface):
        self.gc.ctx = cairo.Context(surface)
