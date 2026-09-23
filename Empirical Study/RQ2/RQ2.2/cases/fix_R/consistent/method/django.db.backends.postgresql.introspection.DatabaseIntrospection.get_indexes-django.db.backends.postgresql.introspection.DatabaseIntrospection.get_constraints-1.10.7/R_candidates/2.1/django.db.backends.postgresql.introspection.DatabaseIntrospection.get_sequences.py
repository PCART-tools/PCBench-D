    def get_sequences(self, cursor, table_name, table_fields=()):
        sequences = []
        cursor.execute("""
            SELECT s.relname as sequence_name, col.attname
            FROM pg_class s
                JOIN pg_namespace sn ON sn.oid = s.relnamespace
                JOIN pg_depend d ON d.refobjid = s.oid AND d.refclassid='pg_class'::regclass
                JOIN pg_attrdef ad ON ad.oid = d.objid AND d.classid = 'pg_attrdef'::regclass
                JOIN pg_attribute col ON col.attrelid = ad.adrelid AND col.attnum = ad.adnum
                JOIN pg_class tbl ON tbl.oid = ad.adrelid
                JOIN pg_namespace n ON n.oid = tbl.relnamespace
            WHERE s.relkind = 'S'
              AND d.deptype in ('a', 'n')
              AND n.nspname = 'public'
              AND tbl.relname = %s
        """, [table_name])
        for row in cursor.fetchall():
            sequences.append({'name': row[0], 'table': table_name, 'column': row[1]})
        return sequences
