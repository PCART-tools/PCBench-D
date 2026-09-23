    def pick(self, mouseevent):
        if not self.widgetlock.locked():
            self.figure.pick(mouseevent)
