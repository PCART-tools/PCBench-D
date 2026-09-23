    def set_offset_position(self, offset_position):
        """
        Set how offsets are applied.  If *offset_position* is 'screen'
        (default) the offset is applied after the master transform has
        been applied, that is, the offsets are in screen coordinates.
        If offset_position is 'data', the offset is applied before the
        master transform, i.e., the offsets are in data coordinates.
        """
        if offset_position not in ('screen', 'data'):
            raise ValueError("offset_position must be 'screen' or 'data'")
        self._offset_position = offset_position
        self.stale = True
