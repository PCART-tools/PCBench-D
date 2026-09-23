@_api.deprecated("3.3")
class StatusbarWx(StatusbarBase, wx.StatusBar):
    """For use with ToolManager."""
    def __init__(self, parent, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(1)
        self.SetStatusText("")

    def set_message(self, s):
        self.SetStatusText(s)
