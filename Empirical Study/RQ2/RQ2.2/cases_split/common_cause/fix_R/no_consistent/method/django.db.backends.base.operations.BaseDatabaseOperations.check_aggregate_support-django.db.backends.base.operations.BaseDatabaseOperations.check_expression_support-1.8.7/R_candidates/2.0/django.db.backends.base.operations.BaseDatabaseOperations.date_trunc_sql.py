    def date_trunc_sql(self, lookup_type, field_name):
        """
        Given a lookup_type of 'year', 'month', or 'day', return the SQL that
        truncates the given date field field_name to a date object with only
        the given specificity.
        """
        raise NotImplementedError('subclasses of BaseDatabaseOperations may require a datetrunc_sql() method')
