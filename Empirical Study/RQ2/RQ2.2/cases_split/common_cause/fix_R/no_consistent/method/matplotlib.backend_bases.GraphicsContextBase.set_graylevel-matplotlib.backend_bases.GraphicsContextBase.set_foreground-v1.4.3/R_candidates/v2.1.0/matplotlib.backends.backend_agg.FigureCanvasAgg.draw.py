    def draw(self):
        """
        Draw the figure using the renderer
        """
        self.renderer = self.get_renderer(cleared=True)
        # acquire a lock on the shared font cache
        RendererAgg.lock.acquire()

        toolbar = self.toolbar
        try:
            if toolbar:
                toolbar.set_cursor(cursors.WAIT)
            self.figure.draw(self.renderer)
        finally:
            if toolbar:
                toolbar.set_cursor(toolbar._lastCursor)
            RendererAgg.lock.release()
