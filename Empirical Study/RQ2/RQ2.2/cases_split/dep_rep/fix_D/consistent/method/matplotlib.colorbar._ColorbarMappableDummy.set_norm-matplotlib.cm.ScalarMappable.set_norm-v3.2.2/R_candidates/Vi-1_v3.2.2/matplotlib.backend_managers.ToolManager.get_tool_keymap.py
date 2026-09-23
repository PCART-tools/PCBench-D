    def get_tool_keymap(self, name):
        """
        Get the keymap associated with the specified tool.

        Parameters
        ----------
        name : str
            Name of the Tool.

        Returns
        -------
        list : list of keys associated with the Tool
        """

        keys = [k for k, i in self._keys.items() if i == name]
        return keys
