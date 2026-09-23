    def get_new_connection(self, conn_params):
        return Database.connect(
            user=self.settings_dict['USER'],
            password=self.settings_dict['PASSWORD'],
            dsn=self._dsn(),
            **conn_params,
        )
