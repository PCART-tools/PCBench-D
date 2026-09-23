    def contains(self, mouseevent):
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info
        # Maybe the dictionary should allow one to
        # distinguish between a text hit and a vector hit.
        if (self.text.contains(mouseevent)[0] or
                self.vector.contains(mouseevent)[0]):
            return True, {}
        return False, {}
