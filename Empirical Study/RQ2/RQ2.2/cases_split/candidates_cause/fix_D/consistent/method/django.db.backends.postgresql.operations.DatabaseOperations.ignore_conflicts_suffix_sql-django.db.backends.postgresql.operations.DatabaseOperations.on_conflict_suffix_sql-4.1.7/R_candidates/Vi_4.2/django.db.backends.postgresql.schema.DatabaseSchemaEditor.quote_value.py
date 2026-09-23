    def quote_value(self, value):
        if isinstance(value, str):
            value = value.replace("%", "%%")
        return sql.quote(value, self.connection.connection)
