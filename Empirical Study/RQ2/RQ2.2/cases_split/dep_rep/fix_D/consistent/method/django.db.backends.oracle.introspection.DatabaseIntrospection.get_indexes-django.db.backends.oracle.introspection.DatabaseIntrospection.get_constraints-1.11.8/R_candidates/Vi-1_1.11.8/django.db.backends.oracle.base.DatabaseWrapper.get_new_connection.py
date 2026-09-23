    def get_new_connection(self, conn_params):
        return Database.connect(self._connect_string(), **conn_params)
