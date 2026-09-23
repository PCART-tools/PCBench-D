    @_api.deprecated("3.6", alternative="Axes.figure.canvas.get_renderer()")
    def get_renderer_cache(self):
        return self.figure.canvas.get_renderer()
