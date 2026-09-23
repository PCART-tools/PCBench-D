    def _clone_test_db(self, suffix, verbosity, keepdb=False):
        source_database_name = self.connection.settings_dict['NAME']
        target_database_name = self.get_test_db_clone_settings(suffix)['NAME']
        # Forking automatically makes a copy of an in-memory database.
        if not self.is_in_memory_db(source_database_name):
            # Erase the old test database
            if os.access(target_database_name, os.F_OK):
                if keepdb:
                    return
                if verbosity >= 1:
                    print("Destroying old test database for alias %s..." % (
                        self._get_database_display_str(verbosity, target_database_name),
                    ))
                try:
                    os.remove(target_database_name)
                except Exception as e:
                    sys.stderr.write("Got an error deleting the old test database: %s\n" % e)
                    sys.exit(2)
            try:
                shutil.copy(source_database_name, target_database_name)
            except Exception as e:
                sys.stderr.write("Got an error cloning the test database: %s\n" % e)
                sys.exit(2)
