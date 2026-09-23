    def pan(self):
        super().pan()
        self.canvas.send_event('navigate_mode', mode=self.mode.name)
