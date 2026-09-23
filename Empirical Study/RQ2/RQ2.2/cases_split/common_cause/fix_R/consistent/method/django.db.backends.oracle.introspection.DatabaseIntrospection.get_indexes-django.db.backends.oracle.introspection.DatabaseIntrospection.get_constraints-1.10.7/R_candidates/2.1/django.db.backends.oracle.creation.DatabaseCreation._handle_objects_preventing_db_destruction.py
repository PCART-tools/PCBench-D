    def _handle_objects_preventing_db_destruction(self, cursor, parameters, verbosity, autoclobber):
        # There are objects in the test tablespace which prevent dropping it
        # The easy fix is to drop the test user -- but are we allowed to do so?
        print("There are objects in the old test database which prevent its destruction.")
        print("If they belong to the test user, deleting the user will allow the test "
              "database to be recreated.")
        print("Otherwise, you will need to find and remove each of these objects, "
              "or use a different tablespace.\n")
        if self._test_user_create():
            if not autoclobber:
                confirm = input("Type 'yes' to delete user %s: " % parameters['user'])
            if autoclobber or confirm == 'yes':
                try:
                    if verbosity >= 1:
                        print("Destroying old test user...")
                    self._destroy_test_user(cursor, parameters, verbosity)
                except Exception as e:
                    sys.stderr.write("Got an error destroying the test user: %s\n" % e)
                    sys.exit(2)
                try:
                    if verbosity >= 1:
                        print("Destroying old test database for alias '%s'..." % self.connection.alias)
                    self._execute_test_db_destruction(cursor, parameters, verbosity)
                except Exception as e:
                    sys.stderr.write("Got an error destroying the test database: %s\n" % e)
                    sys.exit(2)
            else:
                print("Tests cancelled -- test database cannot be recreated.")
                sys.exit(1)
        else:
            print("Django is configured to use pre-existing test user '%s',"
                  " and will not attempt to delete it.\n" % parameters['user'])
            print("Tests cancelled -- test database cannot be recreated.")
            sys.exit(1)
