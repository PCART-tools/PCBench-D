    def home(self):
        """Recall the first view and position from the stack."""
        self.views[self.figure].home()
        self.positions[self.figure].home()
