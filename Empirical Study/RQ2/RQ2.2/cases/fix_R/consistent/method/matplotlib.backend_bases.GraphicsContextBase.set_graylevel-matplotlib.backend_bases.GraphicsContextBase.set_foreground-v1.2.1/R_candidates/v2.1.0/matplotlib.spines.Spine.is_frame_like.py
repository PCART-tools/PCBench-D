    def is_frame_like(self):
        """return True if directly on axes frame

        This is useful for determining if a spine is the edge of an
        old style MPL plot. If so, this function will return True.
        """
        self._ensure_position_is_set()
        position = self._position
        if isinstance(position, six.string_types):
            if position == 'center':
                position = ('axes', 0.5)
            elif position == 'zero':
                position = ('data', 0)
        if len(position) != 2:
            raise ValueError("position should be 2-tuple")
        position_type, amount = position
        if position_type == 'outward' and amount == 0:
            return True
        else:
            return False
