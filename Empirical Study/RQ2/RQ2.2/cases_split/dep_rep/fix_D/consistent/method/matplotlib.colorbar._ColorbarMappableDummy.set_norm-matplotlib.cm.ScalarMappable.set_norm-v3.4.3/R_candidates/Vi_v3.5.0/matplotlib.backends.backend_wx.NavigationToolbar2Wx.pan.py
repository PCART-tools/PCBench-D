    def pan(self, *args):
        tool = self.wx_ids['Pan']
        self.ToggleTool(tool, not self.GetToolState(tool))
        super().pan(*args)
