    def savepoint_create_sql(self, sid):
        return "SAVEPOINT " + self.quote_name(sid)
