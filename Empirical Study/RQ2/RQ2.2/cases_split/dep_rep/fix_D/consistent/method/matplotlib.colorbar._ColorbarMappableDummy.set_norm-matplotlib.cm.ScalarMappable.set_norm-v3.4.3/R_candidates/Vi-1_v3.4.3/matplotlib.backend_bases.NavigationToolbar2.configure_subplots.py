    def configure_subplots(self, *args):
        plt = _safe_pyplot_import()
        self.subplot_tool = plt.subplot_tool(self.canvas.figure)
        self.subplot_tool.figure.canvas.manager.show()
