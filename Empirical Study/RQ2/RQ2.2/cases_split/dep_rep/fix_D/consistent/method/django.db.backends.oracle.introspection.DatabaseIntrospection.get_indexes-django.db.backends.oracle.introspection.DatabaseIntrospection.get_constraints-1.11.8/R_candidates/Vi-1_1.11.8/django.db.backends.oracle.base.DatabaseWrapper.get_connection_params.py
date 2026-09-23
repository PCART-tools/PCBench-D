    def get_connection_params(self):
        # Specify encoding to support unicode in DSN.
        conn_params = {'encoding': 'UTF-8', 'nencoding': 'UTF-8'}
        user_params = self.settings_dict['OPTIONS'].copy()
        if 'use_returning_into' in user_params:
            del user_params['use_returning_into']
        conn_params.update(user_params)
        return conn_params
