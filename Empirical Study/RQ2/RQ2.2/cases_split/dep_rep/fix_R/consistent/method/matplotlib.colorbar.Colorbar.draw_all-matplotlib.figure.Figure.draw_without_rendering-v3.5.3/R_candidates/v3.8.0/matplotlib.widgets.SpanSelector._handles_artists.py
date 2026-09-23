    @property
    def _handles_artists(self):
        if self._edge_handles is not None:
            return self._edge_handles.artists
        else:
            return ()
