    def set_context(self, ctx):
        self.gc.ctx = backend_cairo._to_context(ctx)
