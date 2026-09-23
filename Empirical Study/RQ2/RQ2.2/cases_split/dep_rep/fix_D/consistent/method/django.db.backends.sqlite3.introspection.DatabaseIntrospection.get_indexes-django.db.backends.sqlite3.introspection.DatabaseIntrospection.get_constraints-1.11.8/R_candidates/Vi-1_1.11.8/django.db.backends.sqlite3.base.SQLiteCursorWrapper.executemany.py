    def executemany(self, query, param_list):
        query = self.convert_query(query)
        return Database.Cursor.executemany(self, query, param_list)
