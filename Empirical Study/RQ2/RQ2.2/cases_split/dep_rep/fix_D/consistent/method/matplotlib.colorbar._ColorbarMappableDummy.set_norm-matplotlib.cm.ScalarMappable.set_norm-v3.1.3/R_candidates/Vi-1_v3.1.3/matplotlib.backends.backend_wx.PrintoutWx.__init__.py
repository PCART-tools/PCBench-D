    def __init__(self, canvas, width=5.5, margin=0.5, title='matplotlib'):
        wx.Printout.__init__(self, title=title)
        self.canvas = canvas
        # width, in inches of output figure (approximate)
        self.width = width
        self.margin = margin
