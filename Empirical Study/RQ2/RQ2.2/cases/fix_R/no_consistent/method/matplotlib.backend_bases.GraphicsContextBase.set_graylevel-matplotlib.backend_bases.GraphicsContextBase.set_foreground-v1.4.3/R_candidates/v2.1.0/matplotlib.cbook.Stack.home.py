    def home(self):
        """push the first element onto the top of the stack"""
        if not len(self._elements):
            return
        self.push(self._elements[0])
        return self()
