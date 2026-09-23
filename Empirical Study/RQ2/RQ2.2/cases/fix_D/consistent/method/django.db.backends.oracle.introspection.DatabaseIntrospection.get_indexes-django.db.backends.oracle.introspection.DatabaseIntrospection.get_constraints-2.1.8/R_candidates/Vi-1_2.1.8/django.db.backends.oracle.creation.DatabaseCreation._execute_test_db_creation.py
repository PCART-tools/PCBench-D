    def _execute_test_db_creation(self, cursor, parameters, verbosity, keepdb=False):
        if verbosity >= 2:
            print("_create_test_db(): dbname = %s" % parameters['user'])
        statements = [
            """CREATE TABLESPACE %(tblspace)s
               DATAFILE '%(datafile)s' SIZE %(size)s
               REUSE AUTOEXTEND ON NEXT %(extsize)s MAXSIZE %(maxsize)s
            """,
            """CREATE TEMPORARY TABLESPACE %(tblspace_temp)s
               TEMPFILE '%(datafile_tmp)s' SIZE %(size_tmp)s
               REUSE AUTOEXTEND ON NEXT %(extsize_tmp)s MAXSIZE %(maxsize_tmp)s
            """,
        ]
        # Ignore "tablespace already exists" error when keepdb is on.
        acceptable_ora_err = 'ORA-01543' if keepdb else None
        self._execute_allow_fail_statements(cursor, statements, parameters, verbosity, acceptable_ora_err)
