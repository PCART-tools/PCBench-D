    def get_cursor_data(self, event):
        contained, info = self.contains(event)
        if len(info["ind"]) == 1:
            ind, = info["ind"]
            return self.get_array()[ind]
        else:
            return None
