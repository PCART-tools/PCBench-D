    def get_indexes(self, cursor, table_name):
        indexes = {}
        for info in self._table_info(cursor, table_name):
            if info['pk'] != 0:
                indexes[info['name']] = {'primary_key': True,
                                         'unique': False}
        cursor.execute('PRAGMA index_list(%s)' % self.connection.ops.quote_name(table_name))
        # seq, name, unique
        for index, unique in [(field[1], field[2]) for field in cursor.fetchall()]:
            cursor.execute('PRAGMA index_info(%s)' % self.connection.ops.quote_name(index))
            info = cursor.fetchall()
            # Skip indexes across multiple fields
            if len(info) != 1:
                continue
            name = info[0][2]  # seqno, cid, name
            indexes[name] = {'primary_key': indexes.get(name, {}).get("primary_key", False),
                             'unique': unique}
        return indexes
