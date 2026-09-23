    def savepoint_rollback_sql(self, sid):
        return "ROLLBACK TO SAVEPOINT " + self.quote_name(sid)
