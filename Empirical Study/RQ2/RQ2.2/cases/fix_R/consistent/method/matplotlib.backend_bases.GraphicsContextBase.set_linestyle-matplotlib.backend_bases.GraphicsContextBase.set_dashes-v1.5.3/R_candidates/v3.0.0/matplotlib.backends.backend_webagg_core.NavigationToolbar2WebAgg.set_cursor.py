    def set_cursor(self, cursor):
        if cursor != self.cursor:
            self.canvas.send_event("cursor", cursor=cursor)
        self.cursor = cursor
