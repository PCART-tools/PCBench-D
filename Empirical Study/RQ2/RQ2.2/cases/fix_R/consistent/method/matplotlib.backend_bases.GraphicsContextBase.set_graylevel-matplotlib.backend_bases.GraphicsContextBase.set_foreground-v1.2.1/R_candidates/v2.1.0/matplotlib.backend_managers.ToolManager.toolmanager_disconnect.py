    def toolmanager_disconnect(self, cid):
        """
        Disconnect callback id *cid*

        Example usage::

            cid = toolmanager.toolmanager_connect('tool_trigger_zoom',
                                                  on_press)
            #...later
            toolmanager.toolmanager_disconnect(cid)
        """
        return self._callbacks.disconnect(cid)
