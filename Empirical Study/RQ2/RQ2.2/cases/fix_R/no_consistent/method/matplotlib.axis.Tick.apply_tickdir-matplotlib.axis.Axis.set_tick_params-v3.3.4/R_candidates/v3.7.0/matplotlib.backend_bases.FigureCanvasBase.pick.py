    @_api.deprecated("3.6", alternative="canvas.figure.pick")
    def pick(self, mouseevent):
        if not self.widgetlock.locked():
            self.figure.pick(mouseevent)
