    def db_parameters(self, connection):
        return {"type": self.db_type(connection), "check": self.db_check(connection)}
