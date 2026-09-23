@_api.deprecated("3.3")
class StatusBarWx(wx.StatusBar):
    """
    A status bar is added to _FigureFrame to allow measurements and the
    previously selected scroll function to be displayed as a user convenience.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, -1)
        self.SetFieldsCount(2)

    def set_function(self, string):
        self.SetStatusText("%s" % string, 1)
