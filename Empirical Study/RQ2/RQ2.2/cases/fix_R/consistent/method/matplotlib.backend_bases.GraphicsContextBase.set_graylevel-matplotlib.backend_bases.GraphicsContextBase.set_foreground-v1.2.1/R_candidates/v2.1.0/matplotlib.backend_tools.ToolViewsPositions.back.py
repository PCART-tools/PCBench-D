    def back(self):
        """Back one step in the stack of views and positions"""
        self.views[self.figure].back()
        self.positions[self.figure].back()
