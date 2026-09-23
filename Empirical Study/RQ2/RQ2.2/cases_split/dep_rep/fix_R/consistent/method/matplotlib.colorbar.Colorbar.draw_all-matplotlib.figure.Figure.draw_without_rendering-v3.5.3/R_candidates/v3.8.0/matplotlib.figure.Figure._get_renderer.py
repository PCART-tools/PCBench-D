    def _get_renderer(self):
        if hasattr(self.canvas, 'get_renderer'):
            return self.canvas.get_renderer()
        else:
            return _get_renderer(self)
