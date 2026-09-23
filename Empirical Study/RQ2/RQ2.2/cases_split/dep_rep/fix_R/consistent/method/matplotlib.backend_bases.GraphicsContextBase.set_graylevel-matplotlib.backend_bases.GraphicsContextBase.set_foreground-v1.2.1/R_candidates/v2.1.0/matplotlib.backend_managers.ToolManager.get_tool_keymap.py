    def get_tool_keymap(self, name):
        """
        Get the keymap associated with the specified tool

        Parameters
        ----------
        name : string
            Name of the Tool

        Returns
        -------
        list : list of keys associated with the Tool
        """

        keys = [k for k, i in six.iteritems(self._keys) if i == name]
        return keys
