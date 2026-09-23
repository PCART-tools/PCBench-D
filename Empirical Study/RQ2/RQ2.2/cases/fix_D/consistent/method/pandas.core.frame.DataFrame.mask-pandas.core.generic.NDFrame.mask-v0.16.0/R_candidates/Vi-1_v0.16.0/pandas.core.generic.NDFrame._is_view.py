    @property
    def _is_view(self):
        """ boolean : return if I am a view of another array """
        return self._data.is_view
