    @property
    def _nodb_connection(self):
        """
        Return an alternative connection to be used when there is no need to
        access the main database, specifically for test db creation/deletion.
        This also prevents the production database from being exposed to
        potential child threads while (or after) the test database is destroyed.
        Refs #10868, #17786, #16969.
        """
        settings_dict = self.settings_dict.copy()
        settings_dict['NAME'] = None
        nodb_connection = self.__class__(
            settings_dict,
            alias=NO_DB_ALIAS,
            allow_thread_sharing=False)
        return nodb_connection
