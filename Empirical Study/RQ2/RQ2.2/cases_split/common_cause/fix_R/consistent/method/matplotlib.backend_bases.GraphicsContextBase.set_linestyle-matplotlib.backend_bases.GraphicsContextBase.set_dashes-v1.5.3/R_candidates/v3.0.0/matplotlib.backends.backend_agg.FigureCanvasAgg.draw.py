    def draw(self):
        """
        Draw the figure using the renderer.
        """
        self.renderer = self.get_renderer(cleared=True)
        # acquire a lock on the shared font cache
        RendererAgg.lock.acquire()

        toolbar = self.toolbar
        try:
            self.figure.draw(self.renderer)
            # A GUI class may be need to update a window using this draw, so
            # don't forget to call the superclass.
            super().draw()
        finally:
            RendererAgg.lock.release()
