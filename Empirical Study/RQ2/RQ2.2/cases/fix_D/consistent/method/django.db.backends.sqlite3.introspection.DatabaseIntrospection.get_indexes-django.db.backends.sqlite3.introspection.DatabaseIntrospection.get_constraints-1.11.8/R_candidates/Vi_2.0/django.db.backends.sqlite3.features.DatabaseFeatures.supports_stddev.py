    @cached_property
    def supports_stddev(self):
        """
        Confirm support for STDDEV and related stats functions.

        SQLite supports STDDEV as an extension package; so
        connection.ops.check_expression_support() can't unilaterally
        rule out support for STDDEV. Manually check whether the call works.
        """
        with self.connection.cursor() as cursor:
            cursor.execute('CREATE TABLE STDDEV_TEST (X INT)')
            try:
                cursor.execute('SELECT STDDEV(*) FROM STDDEV_TEST')
                has_support = True
            except utils.DatabaseError:
                has_support = False
            cursor.execute('DROP TABLE STDDEV_TEST')
        return has_support
