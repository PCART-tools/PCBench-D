    def draw(self):
        if self.get_visible() and self.get_mapped():
            allocation = self.get_allocation()
            self._render_figure(allocation.width, allocation.height)
        super().draw()
