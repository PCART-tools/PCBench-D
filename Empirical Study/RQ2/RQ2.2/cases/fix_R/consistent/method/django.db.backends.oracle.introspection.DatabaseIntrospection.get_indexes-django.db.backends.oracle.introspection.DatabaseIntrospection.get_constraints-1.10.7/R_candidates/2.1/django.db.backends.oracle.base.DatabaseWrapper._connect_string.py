    def _connect_string(self):
        return '%s/\\"%s\\"@%s' % (self.settings_dict['USER'], self.settings_dict['PASSWORD'], self._dsn())
