    def disable(self, event):
        self.set_scale(event.inaxes, 'linear')
        self.figure.canvas.draw_idle()
