    def _handle_toggle(self, tool, sender, canvasevent, data):
        """
        Toggle tools, need to untoggle prior to using other Toggle tool.
        Called from trigger_tool.

        Parameters
        ----------
        tool : Tool object
        sender : object
            Object that wishes to trigger the tool
        canvasevent : Event
            Original Canvas event or None
        data : Object
            Extra data to pass to the tool when triggering
        """

        radio_group = tool.radio_group
        # radio_group None is not mutually exclusive
        # just keep track of toggled tools in this group
        if radio_group is None:
            if tool.name in self._toggled[None]:
                self._toggled[None].remove(tool.name)
            else:
                self._toggled[None].add(tool.name)
            return

        # If the tool already has a toggled state, untoggle it
        if self._toggled[radio_group] == tool.name:
            toggled = None
        # If no tool was toggled in the radio_group
        # toggle it
        elif self._toggled[radio_group] is None:
            toggled = tool.name
        # Other tool in the radio_group is toggled
        else:
            # Untoggle previously toggled tool
            self.trigger_tool(self._toggled[radio_group],
                              self,
                              canvasevent,
                              data)
            toggled = tool.name

        # Keep track of the toggled tool in the radio_group
        self._toggled[radio_group] = toggled
