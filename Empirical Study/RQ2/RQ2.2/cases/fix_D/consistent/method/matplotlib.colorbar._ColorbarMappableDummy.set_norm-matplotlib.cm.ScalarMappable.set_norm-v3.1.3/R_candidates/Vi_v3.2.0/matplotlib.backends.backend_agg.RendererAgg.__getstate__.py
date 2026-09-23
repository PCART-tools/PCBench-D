    def __getstate__(self):
        # We only want to preserve the init keywords of the Renderer.
        # Anything else can be re-created.
        return {'width': self.width, 'height': self.height, 'dpi': self.dpi}
