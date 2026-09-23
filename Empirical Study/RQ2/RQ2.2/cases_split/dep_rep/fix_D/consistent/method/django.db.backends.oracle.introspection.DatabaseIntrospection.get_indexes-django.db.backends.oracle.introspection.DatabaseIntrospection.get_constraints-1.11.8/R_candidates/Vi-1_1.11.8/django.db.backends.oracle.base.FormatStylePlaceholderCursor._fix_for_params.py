    def _fix_for_params(self, query, params, unify_by_values=False):
        # cx_Oracle wants no trailing ';' for SQL statements.  For PL/SQL, it
        # it does want a trailing ';' but not a trailing '/'.  However, these
        # characters must be included in the original query in case the query
        # is being passed to SQL*Plus.
        if query.endswith(';') or query.endswith('/'):
            query = query[:-1]
        if params is None:
            params = []
            query = query
        elif hasattr(params, 'keys'):
            # Handle params as dict
            args = {k: ":%s" % k for k in params.keys()}
            query = query % args
        elif unify_by_values and len(params) > 0:
            # Handle params as a dict with unified query parameters by their
            # values. It can be used only in single query execute() because
            # executemany() shares the formatted query with each of the params
            # list. e.g. for input params = [0.75, 2, 0.75, 'sth', 0.75]
            # params_dict = {
            #   (2, <type 'int'>): ':arg2',
            #   (0.75, <type 'float'>): ':arg1',
            #   ('sth', <type 'str'>): ':arg0',
            # }
            # args = [':arg0', ':arg1', ':arg0', ':arg2', ':arg0']
            # params = {':arg0': 0.75, ':arg1': 2, ':arg2': 'sth'}
            params = [(param, type(param)) for param in params]
            params_dict = {param: ':arg%d' % i for i, param in enumerate(set(params))}
            args = [params_dict[param] for param in params]
            params = {value: key[0] for key, value in params_dict.items()}
            query = query % tuple(args)
        else:
            # Handle params as sequence
            args = [(':arg%d' % i) for i in range(len(params))]
            query = query % tuple(args)
        return force_text(query, self.charset), self._format_params(params)
