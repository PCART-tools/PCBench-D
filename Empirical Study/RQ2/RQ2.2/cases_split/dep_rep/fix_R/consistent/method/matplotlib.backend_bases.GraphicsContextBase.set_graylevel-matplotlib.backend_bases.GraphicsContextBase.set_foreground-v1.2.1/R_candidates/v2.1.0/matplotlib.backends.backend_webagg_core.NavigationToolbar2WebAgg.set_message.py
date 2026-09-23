    def set_message(self, message):
        if message != self.message:
            self.canvas.send_event("message", message=message)
        self.message = message
