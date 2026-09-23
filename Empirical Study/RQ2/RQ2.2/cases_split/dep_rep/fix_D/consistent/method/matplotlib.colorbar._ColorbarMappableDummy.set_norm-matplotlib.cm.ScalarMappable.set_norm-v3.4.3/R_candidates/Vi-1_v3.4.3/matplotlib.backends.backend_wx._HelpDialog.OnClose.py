    def OnClose(self, event):
        _HelpDialog._instance = None  # remove global reference
        self.DestroyLater()
        event.Skip()
