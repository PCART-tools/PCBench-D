    def limit_offset_sql(self, low_mark, high_mark):
        fetch, offset = self._get_limit_offset_params(low_mark, high_mark)
        return '%s%s' % (
            (' OFFSET %d ROWS' % offset) if offset else '',
            (' FETCH FIRST %d ROWS ONLY' % fetch) if fetch else '',
        )
