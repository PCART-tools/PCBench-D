    def __init__(self, parent, *args, **kwargs):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(2)
        self.SetStatusText("None", 1)
