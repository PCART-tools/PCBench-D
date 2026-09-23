    def trigger(self, *args, **kwargs):
        pixmap = self.canvas.grab()
        qApp.clipboard().setPixmap(pixmap)
