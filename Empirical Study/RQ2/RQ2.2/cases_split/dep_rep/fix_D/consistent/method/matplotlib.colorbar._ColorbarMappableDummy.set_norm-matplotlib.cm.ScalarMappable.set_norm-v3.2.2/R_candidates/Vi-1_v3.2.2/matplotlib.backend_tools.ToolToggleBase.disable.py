    def disable(self, event=None):
        """
        Disable the toggle tool

        `trigger` call this method when `toggled` is True.

        This can happen in different circumstances

        * Click on the toolbar tool button
        * Call to `matplotlib.backend_managers.ToolManager.trigger_tool`
        * Another `ToolToggleBase` derived tool is triggered
          (from the same `ToolManager`)
        """
        pass
