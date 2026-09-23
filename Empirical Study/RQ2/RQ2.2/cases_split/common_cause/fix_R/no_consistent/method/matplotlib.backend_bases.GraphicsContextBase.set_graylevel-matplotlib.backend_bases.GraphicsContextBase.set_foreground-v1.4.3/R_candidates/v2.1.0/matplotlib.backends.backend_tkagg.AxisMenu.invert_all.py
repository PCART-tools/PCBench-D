    def invert_all(self):
        for a in self._axis_var:
            a.set(not a.get())
        self.set_active()
