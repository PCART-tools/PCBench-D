    def __unicode__(self):
        scope_keys = _get_pretty_string(list(self.scope.keys()))
        res_keys = _get_pretty_string(list(self.resolvers.keys()))
        return '%s(scope=%s, resolvers=%s)' % (type(self).__name__, scope_keys,
                                               res_keys)
