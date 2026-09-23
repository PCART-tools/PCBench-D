    def _dsn(self):
        settings_dict = self.settings_dict
        if not settings_dict['HOST'].strip():
            settings_dict['HOST'] = 'localhost'
        if settings_dict['PORT']:
            return Database.makedsn(settings_dict['HOST'], int(settings_dict['PORT']), settings_dict['NAME'])
        return settings_dict['NAME']
