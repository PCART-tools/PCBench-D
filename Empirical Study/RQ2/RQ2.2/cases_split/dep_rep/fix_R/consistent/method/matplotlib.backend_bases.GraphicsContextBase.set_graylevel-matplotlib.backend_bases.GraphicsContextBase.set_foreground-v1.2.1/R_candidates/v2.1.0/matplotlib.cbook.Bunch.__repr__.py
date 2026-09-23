    def __repr__(self):
        return 'Bunch(%s)' % ', '.join(
            '%s=%s' % kv for kv in six.iteritems(vars(self)))
