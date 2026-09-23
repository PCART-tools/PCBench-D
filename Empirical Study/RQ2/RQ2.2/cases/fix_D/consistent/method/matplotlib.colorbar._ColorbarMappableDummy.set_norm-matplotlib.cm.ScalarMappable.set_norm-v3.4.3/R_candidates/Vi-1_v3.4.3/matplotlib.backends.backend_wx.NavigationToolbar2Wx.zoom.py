    def zoom(self, *args):
        tool = self.wx_ids['Zoom']
        self.ToggleTool(tool, not self.GetToolState(tool))
        super().zoom(*args)
