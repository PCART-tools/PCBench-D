    def enable(self, event):
        self.set_scale(event.inaxes, 'log')
        self.figure.canvas.draw_idle()
