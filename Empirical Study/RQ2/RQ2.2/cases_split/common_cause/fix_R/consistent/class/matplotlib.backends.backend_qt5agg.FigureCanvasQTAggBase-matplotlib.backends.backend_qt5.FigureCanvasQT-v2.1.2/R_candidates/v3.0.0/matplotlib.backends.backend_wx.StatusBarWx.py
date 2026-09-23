class StatusBarWx(wx.StatusBar):
    """
    A status bar is added to _FigureFrame to allow measurements and the
    previously selected scroll function to be displayed as a user
    convenience.
    """

    def __init__(self, parent, *args, **kwargs):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(2)
        self.SetStatusText("None", 1)
        # self.SetStatusText("Measurement: None", 2)
        # self.Reposition()

    def set_function(self, string):
        self.SetStatusText("%s" % string, 1)
