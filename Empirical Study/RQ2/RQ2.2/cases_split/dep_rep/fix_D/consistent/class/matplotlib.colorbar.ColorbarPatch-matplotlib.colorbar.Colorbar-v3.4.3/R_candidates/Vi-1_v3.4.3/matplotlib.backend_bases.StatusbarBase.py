@_api.deprecated("3.3")
class StatusbarBase:
    """Base class for the statusbar."""
    def __init__(self, toolmanager):
        self.toolmanager = toolmanager
        self.toolmanager.toolmanager_connect('tool_message_event',
                                             self._message_cbk)

    def _message_cbk(self, event):
        """Capture the 'tool_message_event' and set the message."""
        self.set_message(event.message)

    def set_message(self, s):
        """
        Display a message on toolbar or in status bar.

        Parameters
        ----------
        s : str
            Message text.
        """
