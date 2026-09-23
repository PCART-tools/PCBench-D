    def get_connection_params(self):
        settings_dict = self.settings_dict
        # None may be used to connect to the default 'postgres' db
        if settings_dict['NAME'] == '':
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply the NAME value.")
        if len(settings_dict['NAME'] or '') > self.ops.max_name_length():
            raise ImproperlyConfigured(
                'Database names longer than %d characters are not supported by '
                'PostgreSQL. Supply a shorter NAME in settings.DATABASES.'
                % self.ops.max_name_length()
            )
        conn_params = {
            'database': settings_dict['NAME'] or 'postgres',
            **settings_dict['OPTIONS'],
        }
        conn_params.pop('isolation_level', None)
        if settings_dict['USER']:
            conn_params['user'] = settings_dict['USER']
        if settings_dict['PASSWORD']:
            conn_params['password'] = settings_dict['PASSWORD']
        if settings_dict['HOST']:
            conn_params['host'] = settings_dict['HOST']
        if settings_dict['PORT']:
            conn_params['port'] = settings_dict['PORT']
        return conn_params
