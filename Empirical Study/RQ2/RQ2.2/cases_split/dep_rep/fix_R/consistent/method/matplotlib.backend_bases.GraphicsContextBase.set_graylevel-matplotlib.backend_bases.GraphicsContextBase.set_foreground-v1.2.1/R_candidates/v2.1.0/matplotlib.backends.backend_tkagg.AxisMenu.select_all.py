    def select_all(self):
        for a in self._axis_var:
            a.set(1)
        self.set_active()
