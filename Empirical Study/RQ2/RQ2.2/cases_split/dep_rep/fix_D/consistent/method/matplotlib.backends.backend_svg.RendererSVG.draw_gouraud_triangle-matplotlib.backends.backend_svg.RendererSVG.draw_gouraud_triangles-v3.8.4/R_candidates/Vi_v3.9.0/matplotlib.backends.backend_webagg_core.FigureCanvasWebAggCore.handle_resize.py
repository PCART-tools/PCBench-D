    def handle_resize(self, event):
        x = int(event.get('width', 800)) * self.device_pixel_ratio
        y = int(event.get('height', 800)) * self.device_pixel_ratio
        fig = self.figure
        # An attempt at approximating the figure size in pixels.
        fig.set_size_inches(x / fig.dpi, y / fig.dpi, forward=False)
        # Acknowledge the resize, and force the viewer to update the
        # canvas size to the figure's new size (which is hopefully
        # identical or within a pixel or so).
        self._png_is_old = True
        self.manager.resize(*fig.bbox.size, forward=False)
        ResizeEvent('resize_event', self)._process()
        self.draw_idle()
