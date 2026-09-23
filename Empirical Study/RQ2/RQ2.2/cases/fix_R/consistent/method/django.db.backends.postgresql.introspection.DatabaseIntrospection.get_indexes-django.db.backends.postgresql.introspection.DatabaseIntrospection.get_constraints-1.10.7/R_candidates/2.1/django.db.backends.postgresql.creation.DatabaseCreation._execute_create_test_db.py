    def _execute_create_test_db(self, cursor, parameters, keepdb=False):
        try:
            super()._execute_create_test_db(cursor, parameters, keepdb)
        except Exception as e:
            if getattr(e.__cause__, 'pgcode', '') != errorcodes.DUPLICATE_DATABASE:
                # All errors except "database already exists" cancel tests.
                sys.stderr.write('Got an error creating the test database: %s\n' % e)
                sys.exit(2)
            elif not keepdb:
                # If the database should be kept, ignore "database already
                # exists".
                raise e
