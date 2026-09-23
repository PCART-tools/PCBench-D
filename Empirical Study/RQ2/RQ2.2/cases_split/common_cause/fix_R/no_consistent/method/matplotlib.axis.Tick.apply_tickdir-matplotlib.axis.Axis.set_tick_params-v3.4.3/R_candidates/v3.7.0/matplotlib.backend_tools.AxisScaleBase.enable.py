    def enable(self, event=None):
        self.set_scale(event.inaxes, 'log')
        self.figure.canvas.draw_idle()
