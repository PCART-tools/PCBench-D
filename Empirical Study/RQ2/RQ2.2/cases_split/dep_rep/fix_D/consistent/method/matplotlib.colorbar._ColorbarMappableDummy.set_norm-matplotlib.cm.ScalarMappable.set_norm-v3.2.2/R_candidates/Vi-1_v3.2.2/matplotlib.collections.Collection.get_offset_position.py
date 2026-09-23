    def get_offset_position(self):
        """
        Returns how offsets are applied for the collection.  If
        *offset_position* is 'screen', the offset is applied after the
        master transform has been applied, that is, the offsets are in
        screen coordinates.  If offset_position is 'data', the offset
        is applied before the master transform, i.e., the offsets are
        in data coordinates.
        """
        return self._offset_position
