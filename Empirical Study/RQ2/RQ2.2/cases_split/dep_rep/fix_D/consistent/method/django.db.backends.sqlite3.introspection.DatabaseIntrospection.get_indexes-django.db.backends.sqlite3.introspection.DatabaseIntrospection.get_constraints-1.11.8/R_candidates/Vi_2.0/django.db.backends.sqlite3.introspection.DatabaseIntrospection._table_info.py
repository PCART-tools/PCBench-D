    def _table_info(self, cursor, name):
        cursor.execute('PRAGMA table_info(%s)' % self.connection.ops.quote_name(name))
        # cid, name, type, notnull, default_value, pk
        return [{
            'name': field[1],
            'type': field[2],
            'size': get_field_size(field[2]),
            'null_ok': not field[3],
            'default': field[4],
            'pk': field[5],  # undocumented
        } for field in cursor.fetchall()]
