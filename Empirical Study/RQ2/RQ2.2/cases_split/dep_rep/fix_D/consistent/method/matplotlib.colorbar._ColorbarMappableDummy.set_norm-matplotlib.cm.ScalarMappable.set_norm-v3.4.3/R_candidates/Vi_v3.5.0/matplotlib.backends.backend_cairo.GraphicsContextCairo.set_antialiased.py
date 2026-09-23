    def set_antialiased(self, b):
        self.ctx.set_antialias(
            cairo.ANTIALIAS_DEFAULT if b else cairo.ANTIALIAS_NONE)
