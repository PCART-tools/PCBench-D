    def get_indexes(self, cursor, table_name):
        """
        Deprecated in Django 1.11, use get_constraints instead.
        Return a dictionary of indexed fieldname -> infodict for the given
        table, where each infodict is in the format:
            {'primary_key': boolean representing whether it's the primary key,
             'unique': boolean representing whether it's a unique index}

        Only single-column indexes are introspected.
        """
        raise NotImplementedError('subclasses of BaseDatabaseIntrospection may require a get_indexes() method')
