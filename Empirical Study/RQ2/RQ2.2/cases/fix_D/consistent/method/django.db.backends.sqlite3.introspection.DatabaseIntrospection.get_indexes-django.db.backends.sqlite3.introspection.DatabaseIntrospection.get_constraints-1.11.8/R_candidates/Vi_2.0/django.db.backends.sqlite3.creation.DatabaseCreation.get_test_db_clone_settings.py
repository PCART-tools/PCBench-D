    def get_test_db_clone_settings(self, suffix):
        orig_settings_dict = self.connection.settings_dict
        source_database_name = orig_settings_dict['NAME']
        if self.is_in_memory_db(source_database_name):
            return orig_settings_dict
        else:
            new_settings_dict = orig_settings_dict.copy()
            root, ext = os.path.splitext(orig_settings_dict['NAME'])
            new_settings_dict['NAME'] = '{}_{}.{}'.format(root, suffix, ext)
            return new_settings_dict
