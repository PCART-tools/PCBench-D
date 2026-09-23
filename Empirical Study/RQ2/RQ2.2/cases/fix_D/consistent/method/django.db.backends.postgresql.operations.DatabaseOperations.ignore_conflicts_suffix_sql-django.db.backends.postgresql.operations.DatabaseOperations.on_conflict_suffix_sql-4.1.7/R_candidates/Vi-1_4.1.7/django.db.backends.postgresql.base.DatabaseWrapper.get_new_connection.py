    @async_unsafe
    def get_new_connection(self, conn_params):
        connection = Database.connect(**conn_params)

        # self.isolation_level must be set:
        # - after connecting to the database in order to obtain the database's
        #   default when no value is explicitly specified in options.
        # - before calling _set_autocommit() because if autocommit is on, that
        #   will set connection.isolation_level to ISOLATION_LEVEL_AUTOCOMMIT.
        options = self.settings_dict["OPTIONS"]
        try:
            self.isolation_level = options["isolation_level"]
        except KeyError:
            self.isolation_level = connection.isolation_level
        else:
            # Set the isolation level to the value from OPTIONS.
            if self.isolation_level != connection.isolation_level:
                connection.set_session(isolation_level=self.isolation_level)
        # Register dummy loads() to avoid a round trip from psycopg2's decode
        # to json.dumps() to json.loads(), when using a custom decoder in
        # JSONField.
        psycopg2.extras.register_default_jsonb(
            conn_or_curs=connection, loads=lambda x: x
        )
        return connection
