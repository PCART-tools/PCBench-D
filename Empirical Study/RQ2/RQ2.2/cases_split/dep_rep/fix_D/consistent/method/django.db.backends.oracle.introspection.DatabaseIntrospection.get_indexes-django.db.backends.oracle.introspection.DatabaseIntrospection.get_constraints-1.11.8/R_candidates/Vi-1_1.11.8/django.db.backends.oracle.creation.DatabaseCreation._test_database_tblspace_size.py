    def _test_database_tblspace_size(self):
        return self._test_settings_get('DATAFILE_MAXSIZE', default='500M')
