    def _switch_to_test_user(self, parameters):
        """
        Oracle doesn't have the concept of separate databases under the same user.
        Thus, we use a separate user (see _create_test_db). This method is used
        to switch to that user. We will need the main user again for clean-up when
        we end testing, so we keep its credentials in SAVED_USER/SAVED_PASSWORD
        entries in the settings dict.
        """
        real_settings = settings.DATABASES[self.connection.alias]
        real_settings['SAVED_USER'] = self.connection.settings_dict['SAVED_USER'] = \
            self.connection.settings_dict['USER']
        real_settings['SAVED_PASSWORD'] = self.connection.settings_dict['SAVED_PASSWORD'] = \
            self.connection.settings_dict['PASSWORD']
        real_test_settings = real_settings['TEST']
        test_settings = self.connection.settings_dict['TEST']
        real_test_settings['USER'] = real_settings['USER'] = test_settings['USER'] = \
            self.connection.settings_dict['USER'] = parameters['user']
        real_settings['PASSWORD'] = self.connection.settings_dict['PASSWORD'] = parameters['password']
