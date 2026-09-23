    def for_update_sql(self, nowait=False, skip_locked=False, of=()):
        """
        Return the FOR UPDATE SQL clause to lock rows for an update operation.
        """
        return 'FOR UPDATE%s%s%s' % (
            ' OF %s' % ', '.join(of) if of else '',
            ' NOWAIT' if nowait else '',
            ' SKIP LOCKED' if skip_locked else '',
        )
