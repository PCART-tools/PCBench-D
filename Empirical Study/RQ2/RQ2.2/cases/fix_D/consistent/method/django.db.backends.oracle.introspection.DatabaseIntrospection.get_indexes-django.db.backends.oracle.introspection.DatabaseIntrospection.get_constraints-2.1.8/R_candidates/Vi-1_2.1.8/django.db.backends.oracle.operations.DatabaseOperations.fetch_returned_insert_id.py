    def fetch_returned_insert_id(self, cursor):
        try:
            value = cursor._insert_id_var.getvalue()
            # cx_Oracle < 7 returns value, >= 7 returns list with single value.
            return int(value[0] if isinstance(value, list) else value)
        except (IndexError, TypeError):
            # cx_Oracle < 6.3 returns None, >= 6.3 raises IndexError.
            raise DatabaseError(
                'The database did not return a new row id. Probably "ORA-1403: '
                'no data found" was raised internally but was hidden by the '
                'Oracle OCI library (see https://code.djangoproject.com/ticket/28859).'
            )
