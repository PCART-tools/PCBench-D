    def sql_table_creation_suffix(self):
        test_settings = self.connection.settings_dict['TEST']
        assert test_settings['COLLATION'] is None, (
            "PostgreSQL does not support collation setting at database creation time."
        )
        return self._get_database_create_suffix(
            encoding=test_settings['CHARSET'],
            template=test_settings.get('TEMPLATE'),
        )
