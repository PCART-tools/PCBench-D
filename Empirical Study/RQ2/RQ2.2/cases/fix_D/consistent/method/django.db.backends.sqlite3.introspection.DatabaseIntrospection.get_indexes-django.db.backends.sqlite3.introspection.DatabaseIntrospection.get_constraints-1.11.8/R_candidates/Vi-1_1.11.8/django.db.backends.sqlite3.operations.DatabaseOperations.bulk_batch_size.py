    def bulk_batch_size(self, fields, objs):
        """
        SQLite has a compile-time default (SQLITE_LIMIT_VARIABLE_NUMBER) of
        999 variables per query.

        If there's only a single field to insert, the limit is 500
        (SQLITE_MAX_COMPOUND_SELECT).
        """
        limit = 999 if len(fields) > 1 else 500
        return (limit // len(fields)) if len(fields) > 0 else len(objs)
