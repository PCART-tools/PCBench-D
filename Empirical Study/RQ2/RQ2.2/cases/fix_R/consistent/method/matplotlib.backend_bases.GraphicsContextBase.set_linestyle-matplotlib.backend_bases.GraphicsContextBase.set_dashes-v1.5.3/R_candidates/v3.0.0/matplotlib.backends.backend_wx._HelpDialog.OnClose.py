    def OnClose(self, evt):
        _HelpDialog._instance = None  # remove global reference
        self.DestroyLater()
        evt.Skip()
