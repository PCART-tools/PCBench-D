    def return_insert_id(self):
        """
        For backends that support returning the last insert ID as part of an
        insert query, return the SQL and params to append to the INSERT query.
        The returned fragment should contain a format string to hold the
        appropriate column.
        """
        pass
