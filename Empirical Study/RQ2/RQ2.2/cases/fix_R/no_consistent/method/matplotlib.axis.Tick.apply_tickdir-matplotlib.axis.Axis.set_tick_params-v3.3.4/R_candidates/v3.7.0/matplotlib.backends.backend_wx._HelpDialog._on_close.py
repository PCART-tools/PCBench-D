    def _on_close(self, event):
        _HelpDialog._instance = None  # remove global reference
        self.DestroyLater()
        event.Skip()
