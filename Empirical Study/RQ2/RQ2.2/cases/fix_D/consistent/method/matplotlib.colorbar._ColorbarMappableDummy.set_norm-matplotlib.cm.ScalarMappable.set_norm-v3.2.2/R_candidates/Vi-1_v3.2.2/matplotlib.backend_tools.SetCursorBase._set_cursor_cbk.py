    def _set_cursor_cbk(self, event):
        if not event:
            return

        if not getattr(event, 'inaxes', False) or not self._cursor:
            if self._last_cursor != self._default_cursor:
                self.set_cursor(self._default_cursor)
                self._last_cursor = self._default_cursor
        elif self._cursor:
            cursor = self._cursor
            if cursor and self._last_cursor != cursor:
                self.set_cursor(cursor)
                self._last_cursor = cursor
