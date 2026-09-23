    def _connect_string(self):
        settings_dict = self.settings_dict
        if not settings_dict['HOST'].strip():
            settings_dict['HOST'] = 'localhost'
        if settings_dict['PORT']:
            dsn = Database.makedsn(settings_dict['HOST'],
                                   int(settings_dict['PORT']),
                                   settings_dict['NAME'])
        else:
            dsn = settings_dict['NAME']
        return "%s/%s@%s" % (settings_dict['USER'],
                             settings_dict['PASSWORD'], dsn)
