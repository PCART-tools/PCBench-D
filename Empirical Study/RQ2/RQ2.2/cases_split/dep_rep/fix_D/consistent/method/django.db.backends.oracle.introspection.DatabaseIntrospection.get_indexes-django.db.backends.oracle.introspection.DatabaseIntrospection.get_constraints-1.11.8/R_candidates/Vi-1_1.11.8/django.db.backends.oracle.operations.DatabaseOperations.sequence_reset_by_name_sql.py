    def sequence_reset_by_name_sql(self, style, sequences):
        sql = []
        for sequence_info in sequences:
            sequence_name = self._get_sequence_name(sequence_info['table'])
            table_name = self.quote_name(sequence_info['table'])
            column_name = self.quote_name(sequence_info['column'] or 'id')
            query = self._sequence_reset_sql % {
                'sequence': sequence_name,
                'table': table_name,
                'column': column_name,
            }
            sql.append(query)
        return sql
