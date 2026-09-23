    def pick(self, mouseevent):
        if not self.canvas.widgetlock.locked():
            super().pick(mouseevent)
