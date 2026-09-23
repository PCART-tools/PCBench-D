    def toolmanager_connect(self, s, func):
        """
        Connect event with string *s* to *func*.

        Parameters
        ----------
        s : String
            Name of the event

            The following events are recognized

            - 'tool_message_event'
            - 'tool_removed_event'
            - 'tool_added_event'

            For every tool added a new event is created

            - 'tool_trigger_TOOLNAME`
              Where TOOLNAME is the id of the tool.

        func : function
            Function to be called with signature
            def func(event)
        """
        return self._callbacks.connect(s, func)
