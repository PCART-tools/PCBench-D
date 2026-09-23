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

        if is_psycopg3:
            # Register the cursor timezone only if the connection disagrees, to
            # avoid copying the adapter map.
            tzloader = self.connection.adapters.get_loader(TIMESTAMPTZ_OID, Format.TEXT)
            if self.timezone != tzloader.timezone:
                register_tzloader(self.timezone, cursor)
        else:
            cursor.tzinfo_factory = self.tzinfo_factory if settings.USE_TZ else None
        return cursor
