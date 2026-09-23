    def _onKeyUp(self, evt):
        """Release key."""
        key = self._get_key(evt)
        # print 'release key', key
        evt.Skip()
        FigureCanvasBase.key_release_event(self, key, guiEvent=evt)
