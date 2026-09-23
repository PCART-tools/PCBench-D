    def trigger_tool(self, name):
        """
        Trigger the tool

        Parameters
        ----------
        name : str
            Name (id) of the tool triggered from within the container.
        """
        self.toolmanager.trigger_tool(name, sender=self)
