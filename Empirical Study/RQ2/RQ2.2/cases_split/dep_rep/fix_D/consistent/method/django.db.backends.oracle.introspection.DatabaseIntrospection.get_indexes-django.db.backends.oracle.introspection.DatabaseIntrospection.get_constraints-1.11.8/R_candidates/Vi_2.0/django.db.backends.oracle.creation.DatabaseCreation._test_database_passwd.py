    def _test_database_passwd(self):
        password = self._test_settings_get('PASSWORD')
        if password is None and self._test_user_create():
            # Oracle passwords are limited to 30 chars and can't contain symbols.
            password = get_random_string(length=30)
        return password
