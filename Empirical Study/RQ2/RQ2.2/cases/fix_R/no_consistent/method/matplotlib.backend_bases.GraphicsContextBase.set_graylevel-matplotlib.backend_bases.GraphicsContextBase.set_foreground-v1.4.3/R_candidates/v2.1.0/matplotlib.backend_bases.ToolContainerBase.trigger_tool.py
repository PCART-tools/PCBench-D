    def trigger_tool(self, name):
        """
        Trigger the tool

        Parameters
        ----------
        name : String
            Name (id) of the tool triggered from within the container
        """
        self.toolmanager.trigger_tool(name, sender=self)
