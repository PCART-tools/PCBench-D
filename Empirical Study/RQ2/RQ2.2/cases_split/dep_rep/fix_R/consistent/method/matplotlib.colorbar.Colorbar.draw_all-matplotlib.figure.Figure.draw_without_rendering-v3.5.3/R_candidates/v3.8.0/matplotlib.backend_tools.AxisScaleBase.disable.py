    def disable(self, event=None):
        self.set_scale(event.inaxes, 'linear')
        self.figure.canvas.draw_idle()
