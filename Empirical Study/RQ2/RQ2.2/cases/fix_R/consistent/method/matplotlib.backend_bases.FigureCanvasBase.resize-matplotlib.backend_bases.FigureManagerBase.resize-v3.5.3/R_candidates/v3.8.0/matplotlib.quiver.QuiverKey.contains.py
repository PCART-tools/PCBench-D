    def contains(self, mouseevent):
        if self._different_canvas(mouseevent):
            return False, {}
        # Maybe the dictionary should allow one to
        # distinguish between a text hit and a vector hit.
        if (self.text.contains(mouseevent)[0] or
                self.vector.contains(mouseevent)[0]):
            return True, {}
        return False, {}
