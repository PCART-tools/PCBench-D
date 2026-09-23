    def __init__(self, parent, *args, **kwargs):
        StatusbarBase.__init__(self, *args, **kwargs)
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(1)
        self.SetStatusText("")
