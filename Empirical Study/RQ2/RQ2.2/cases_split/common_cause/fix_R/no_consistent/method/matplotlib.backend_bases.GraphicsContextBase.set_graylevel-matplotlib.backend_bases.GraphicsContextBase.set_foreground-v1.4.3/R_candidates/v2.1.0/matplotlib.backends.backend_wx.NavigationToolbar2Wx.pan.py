    def pan(self, *args):
        self.ToggleTool(self.wx_ids['Zoom'], False)
        NavigationToolbar2.pan(self, *args)
