    def __init__(self, *args, **kwargs):
        self._toggled = kwargs.pop('toggled', self.default_toggled)
        ToolBase.__init__(self, *args, **kwargs)
