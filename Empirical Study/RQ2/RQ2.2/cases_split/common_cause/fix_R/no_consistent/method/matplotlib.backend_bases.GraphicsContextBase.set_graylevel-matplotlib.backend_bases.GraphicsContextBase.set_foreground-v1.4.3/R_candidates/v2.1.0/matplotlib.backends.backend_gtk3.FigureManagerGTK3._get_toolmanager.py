    def _get_toolmanager(self):
        # must be initialised after toolbar has been setted
        if rcParams['toolbar'] == 'toolmanager':
            toolmanager = ToolManager(self.canvas.figure)
        else:
            toolmanager = None
        return toolmanager
