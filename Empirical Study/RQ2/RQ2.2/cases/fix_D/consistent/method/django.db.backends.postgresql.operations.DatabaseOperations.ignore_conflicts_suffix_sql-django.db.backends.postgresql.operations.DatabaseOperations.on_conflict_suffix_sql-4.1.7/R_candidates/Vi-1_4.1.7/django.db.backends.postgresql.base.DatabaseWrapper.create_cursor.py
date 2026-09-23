    @async_unsafe
    def create_cursor(self, name=None):
        if name:
            # In autocommit mode, the cursor will be used outside of a
            # transaction, hence use a holdable cursor.
            cursor = self.connection.cursor(
                name, scrollable=False, withhold=self.connection.autocommit
            )
        else:
            cursor = self.connection.cursor()
        cursor.tzinfo_factory = self.tzinfo_factory if settings.USE_TZ else None
        return cursor
