    def init_connection_state(self):
        super().init_connection_state()
        self.connection.set_client_encoding("UTF8")

        timezone_changed = self.ensure_timezone()
        if timezone_changed:
            # Commit after setting the time zone (see #17062)
            if not self.get_autocommit():
                self.connection.commit()
