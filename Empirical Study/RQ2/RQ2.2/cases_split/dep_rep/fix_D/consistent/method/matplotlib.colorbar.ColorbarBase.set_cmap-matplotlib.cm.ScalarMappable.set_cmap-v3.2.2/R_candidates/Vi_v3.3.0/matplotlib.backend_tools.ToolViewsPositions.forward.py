    def forward(self):
        """Forward one step in the stack of views and positions."""
        self.views[self.figure].forward()
        self.positions[self.figure].forward()
