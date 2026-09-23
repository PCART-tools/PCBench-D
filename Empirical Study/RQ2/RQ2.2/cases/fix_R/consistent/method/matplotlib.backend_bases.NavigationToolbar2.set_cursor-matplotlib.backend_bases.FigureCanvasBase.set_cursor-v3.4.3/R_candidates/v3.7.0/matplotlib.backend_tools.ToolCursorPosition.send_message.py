    def send_message(self, event):
        """Call `matplotlib.backend_managers.ToolManager.message_event`."""
        if self.toolmanager.messagelock.locked():
            return

        from matplotlib.backend_bases import NavigationToolbar2
        message = NavigationToolbar2._mouse_event_to_message(event)
        self.toolmanager.message_event(message, self)
