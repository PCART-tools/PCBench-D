    def __init__(self, name, sender, tool, canvasevent=None, data=None):
        ToolEvent.__init__(self, name, sender, tool, data)
        self.canvasevent = canvasevent
