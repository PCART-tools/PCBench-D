    def draw(self):
        renderer = self.get_renderer(cleared=True)

        self._png_is_old = True

        backend_agg.RendererAgg.lock.acquire()
        try:
            self.figure.draw(renderer)
        finally:
            backend_agg.RendererAgg.lock.release()
            # Swap the frames
            self.manager.refresh_all()
