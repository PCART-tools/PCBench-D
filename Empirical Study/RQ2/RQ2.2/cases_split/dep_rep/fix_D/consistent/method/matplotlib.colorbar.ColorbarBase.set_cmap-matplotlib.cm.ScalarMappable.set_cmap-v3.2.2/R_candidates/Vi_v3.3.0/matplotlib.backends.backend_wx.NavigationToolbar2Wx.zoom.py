    def zoom(self, *args):
        self.ToggleTool(self.wx_ids['Pan'], False)
        NavigationToolbar2.zoom(self, *args)
