    def contains(self, mouseevent):
        for c in self.get_children():
            a, b = c.contains(mouseevent)
            if a:
                return a, b
        return False, {}
