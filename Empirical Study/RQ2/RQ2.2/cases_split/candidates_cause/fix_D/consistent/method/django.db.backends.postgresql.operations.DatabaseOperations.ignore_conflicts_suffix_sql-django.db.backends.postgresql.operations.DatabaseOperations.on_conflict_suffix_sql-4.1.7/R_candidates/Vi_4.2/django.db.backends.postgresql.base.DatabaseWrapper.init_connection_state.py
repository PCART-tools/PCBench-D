    def init_connection_state(self):
        super().init_connection_state()

        # Commit after setting the time zone.
        commit_tz = self.ensure_timezone()
        # Set the role on the connection. This is useful if the credential used
        # to login is not the same as the role that owns database resources. As
        # can be the case when using temporary or ephemeral credentials.
        commit_role = self.ensure_role()

        if (commit_role or commit_tz) and not self.get_autocommit():
            self.connection.commit()
